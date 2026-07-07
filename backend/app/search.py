"""
The core connection-search logic to create iteneraries
"""

from .data import Flight, FlightData
from .timezones import minutes_between, to_utc

MIN_LAYOVER_DOMESTIC_MINUTES = 45
MIN_LAYOVER_INTERNATIONAL_MINUTES = 90
MAX_LAYOVER_MINUTES = 6 * 60
MAX_SEGMENTS = 3  # max stops are 2


def is_domestic(country_a: str, country_b: str) -> bool:
    """True if a connection between these two countries counts as domestic."""
    return country_a == country_b


def _is_valid_connection(data: FlightData, arriving: Flight, departing: Flight) -> bool:
    """
    Check if a flight has a connection from source to destination.
    Checks layover timing for both domestic and international.
    """
    layover_airport = data.get_airport(arriving.destination)
    origin_airport = data.get_airport(arriving.origin)
    final_airport = data.get_airport(departing.destination)

    # Convert time and get layover minutes
    arrive_utc = to_utc(arriving.arrivalTime, layover_airport.timezone)
    depart_utc = to_utc(departing.departureTime, layover_airport.timezone)
    layover = minutes_between(arrive_utc, depart_utc)

    # Get min layover time based on type of flight
    domestic = is_domestic(origin_airport.country, final_airport.country)
    minimum = (
        MIN_LAYOVER_DOMESTIC_MINUTES if domestic else MIN_LAYOVER_INTERNATIONAL_MINUTES
    )

    # Ensure layover is not too short or too long
    if (layover < minimum) or (layover > MAX_LAYOVER_MINUTES):
        return False
    return True


def find_itineraries(
    data: FlightData,
    origin: str,
    destination: str,
    date: str,
) -> list[list[Flight]]:
    """
    Find every valid itinerary from origin to destination on specified date,
    using DFS over the flight graph.

    Approach:
    - Explore one flight at a time from origin on specified date
      (Date filter only applies to first flight)
    - Grow each path one at a time everytime extend is called
    - Recurse into every flight that departs to where we landed at.
    - Save the path and exit once reach destination

    Assumptions
    - No airport changes at a layover, only looking at flights departing from the airport we landed at.
    - No revisiting an airport already in the path example jfk -> lax (no jfk -> ord -> jfk -> lax).
    - Layover timing is within the allowed window (see `_is_valid_connection`).
    - 2 stops maximum per itenerary

    Returns:
    - A list of paths, each a list of Flights
      Example: [ [SP210, SP355], [SP101] ]
    """
    itineraries: list[list[Flight]] = []

    def extend(path: list[Flight]) -> None:
        last = path[-1]

        # Check if reached final destionation
        if last.destination == destination:
            itineraries.append(path)
            return

        # DDont process > 2 stops
        if len(path) >= MAX_SEGMENTS:
            return

        # Keep a set of every visited airport within the node
        visited = set()
        visited.add(path[0].origin)
        for flight in path:
            visited.add(flight.destination)

        # Consider the next flights leaving from airport we just arrived at
        for nxt in data.flights_by_origin.get(last.destination, []):
            if nxt.destination in visited:
                continue
            if not _is_valid_connection(data, last, nxt):
                continue
            extend(path + [nxt])

    # Seed the search from every flight leaving origin on the requested date.
    for flights_from_origin in data.flights_by_origin.get(origin, []):
        # Trim the departure time to just the yyyy-mm-dd (first 10 chars)
        if flights_from_origin.departureTime[:10] == date:
            extend([flights_from_origin])

    return itineraries
