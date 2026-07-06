"""
Turns raw flight sequences from search.py into the API response shape,
then sorts the final list. This is the only module that imports both
the internal Flight type and the Pydantic schemas -- keeps the search
algorithm decoupled from the wire format.
"""

from .data import Flight, FlightData
from .schemas import Itinerary


def build_itinerary(data: FlightData, path: list[Flight]) -> Itinerary:
    """
    Step 5.

    TODO:
    - Map each Flight in `path` to a Segment (same fields, just reshaped).
    - Compute layovers between consecutive segments: for each adjacent pair,
      the airport is the shared arrival/departure airport, and the duration
      is minutes_between(to_utc(arrival), to_utc(next departure)).
    - totalDurationMinutes = minutes_between(to_utc(first departure), to_utc(last arrival)).
    - totalPrice = sum of segment prices.
    """
    raise NotImplementedError


def build_and_sort_itineraries(
    data: FlightData, paths: list[list[Flight]]
) -> list[Itinerary]:
    """
    Step 6.

    TODO: build_itinerary() for each path, then sort the resulting list
    ascending by totalDurationMinutes (shortest first).
    """
    raise NotImplementedError
