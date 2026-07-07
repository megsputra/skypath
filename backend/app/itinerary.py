"""
Formats and cleans up flights objects into itineraries, has information
on each flights, layovers, total travel time and prices.
"""

from .data import Flight, FlightData
from .schemas import Itinerary, Segment, Layover
from .timezones import to_utc, minutes_between


def build_itinerary(data: FlightData, path: list[Flight]) -> Itinerary:
    """
    Maps each Flight in path to a Segment, computes the layover at each
    connection point, and sums up duration/price for the itinerary.
    """

    totalPrice = 0
    segments = []
    for flight in path:
        s = Segment(
            flightNumber=flight.flightNumber,
            airline=flight.airline,
            origin=flight.origin,
            destination=flight.destination,
            departureTime=flight.departureTime,
            arrivalTime=flight.arrivalTime,
            price=flight.price,
        )
        segments.append(s)
        totalPrice += flight.price
    first_flight = path[0]
    last_flight = path[-1]

    layovers = []
    # Compare the flights as pairs
    for arriving, departing in zip(path, path[1:]):
        layover_ariport = data.get_airport(arriving.destination)
        arrive_utc = to_utc(arriving.arrivalTime, layover_ariport.timezone)
        depart_utc = to_utc(departing.departureTime, layover_ariport.timezone)
        layover_dur = minutes_between(arrive_utc, depart_utc)
        layovers.append(
            Layover(airport=layover_ariport.code, durationMinutes=layover_dur)
        )

    origin_tz = data.get_airport(first_flight.origin).timezone
    dest_tz = data.get_airport(last_flight.destination).timezone
    totalDurationMinutes = minutes_between(
        to_utc(first_flight.departureTime, origin_tz),
        to_utc(last_flight.arrivalTime, dest_tz),
    )

    return Itinerary(
        segments=segments,
        layovers=layovers,
        totalDurationMinutes=totalDurationMinutes,
        totalPrice=totalPrice,
    )


def build_and_sort_itineraries(
    data: FlightData, paths: list[list[Flight]]
) -> list[Itinerary]:
    """
    Builds the itenerary for each trip and sorted
    based on shortest travel time
    """

    res = [build_itinerary(data, path) for path in paths]
    res.sort(key=lambda itn: itn.totalDurationMinutes)
    return res
