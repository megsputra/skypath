"""
The core connection-search algorithm: DFS/backtracking over flights,
pruned by the Connection Rules table in instructions.md. Returns raw
flight sequences -- this module has no knowledge of the API response
shape (that's itinerary.py's job).
"""
from .data import Flight, FlightData

MIN_LAYOVER_DOMESTIC_MINUTES = 45
MIN_LAYOVER_INTERNATIONAL_MINUTES = 90
MAX_LAYOVER_MINUTES = 6 * 60
MAX_SEGMENTS = 3 # max stops are 2


def find_itineraries(
    data: FlightData,
    origin: str,
    destination: str,
    date: str,
) -> list[list[Flight]]:
    """
    Step 4.

    TODO:
    DFS/backtracking starting from `origin`, considering only flights whose
    local departure date matches `date` for the first segment. At each hop:
      - only consider flights whose origin == current path's last arrival airport
        (no airport changes during a layover, e.g. JFK -> LGA is invalid)
      - skip airports already visited in this path (no cycles)
      - enforce the layover window using timezones.to_utc() + minutes_between()
        (never compare local-time strings directly): minimum isß
        MIN_LAYOVER_INTERNATIONAL_MINUTES if timezones.is_domestic() is False
        for the two airports involved, else MIN_LAYOVER_DOMESTIC_MINUTES;
        maximum is always MAX_LAYOVER_MINUTES
      - stop extending a path once it has MAX_SEGMENTS flights

    A path is a complete itinerary once its last flight's destination ==
    `destination`. Return every valid path found; don't sort or format
    here -- that's itinerary.py.
    """
    # Flight Data (airport -> flights(origin -> destionation))
    # paths = find_itineraries(flight_data, origin, destination, date)
    raise NotImplementedError
ßß