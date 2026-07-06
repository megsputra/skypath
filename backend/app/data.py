"""
Loads flights.json once at startup and builds the lookup structures the
rest of the app depends on: an airport index (code -> Airport) and a
flight index (origin code -> flights departing from that airport).
"""

import os
import json
from dataclasses import dataclass
from typing import Optional


FLIGHTS_PATH = os.environ.get("FLIGHTS_JSON_PATH", "/data/flights.json")


@dataclass
class Airport:
    code: str
    name: str
    city: str
    country: str
    timezone: str


@dataclass
class Flight:
    flightNumber: str
    airline: str
    origin: str
    destination: str
    departureTime: str  # local ISO string, no UTC offset, e.g. "2024-03-15T08:30:00"
    arrivalTime: str  # local ISO string, no UTC offset
    price: float
    aircraft: str


class FlightData:
    """Holds the loaded dataset plus the indexes derived from it."""

    def __init__(
        self, airports: dict[str, Airport], flights_by_origin: dict[str, list[Flight]]
    ):
        self.airports = airports
        self.flights_by_origin = flights_by_origin

    def get_airport(self, code: str) -> Optional[Airport]:
        return self.airports.get(code)


def load_flight_data(path: str = FLIGHTS_PATH) -> FlightData:
    """
    Step 1 (indexing part) + step 3.

    TODO:
    - Read and parse the JSON file at `path`.
    - Build `airports`: dict of code -> Airport, from the "airports" list.
    - Build `flights_by_origin`: dict of origin code -> list[Flight], from
      the "flights" list, sorted by departureTime. This is what lets
      search.py look up "what can I fly next from here" in O(1) instead of
      scanning all ~300 flights on every recursive hop.
    """
    with open(path) as f:
        flight_data = json.load(f)

    airports = {}
    for airport in flight_data["airports"]:
        airports[airport["code"]] = Airport(**airport)

    flights_by_origin = {}
    for f in flight_data["flights"]:
        flight = Flight(**f)
        # group by origin
        flights_by_origin.setdefault(flight.origin, []).append(flight)

    # sort by departure time
    for fl in flights_by_origin.values():
        fl.sort(key=lambda f: f.departureTime)

    return FlightData(airports, flights_by_origin)
