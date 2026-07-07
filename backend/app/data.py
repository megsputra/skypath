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
    departureTime: str  # local ISO string
    arrivalTime: str
    price: float
    aircraft: str


class FlightData:
    def __init__(
        self, airports: dict[str, Airport], flights_by_origin: dict[str, list[Flight]]
    ):
        self.airports = airports
        self.flights_by_origin = flights_by_origin

    def get_airport(self, code: str) -> Optional[Airport]:
        return self.airports.get(code)


def load_flight_data(path: str = FLIGHTS_PATH) -> FlightData:
    """
    Load flight data from JSON file provided at path.
    Build a dict of airport_code -> Airport object
    Build a dict of origin_code -> List of flights sorted by departure
    This ensures instant look up of flights from a certain airport
    """
    with open(path) as f:
        flight_data = json.load(f)

    airports = {}
    for airport in flight_data["airports"]:
        airports[airport["code"]] = Airport(**airport)

    flights_by_origin = {}
    for f in flight_data["flights"]:
        try:
            price = float(f["price"])
        except (TypeError, ValueError):
            continue
        flight = Flight(**{**f, "price": price})

        # Group flights by origin
        flights_by_origin.setdefault(flight.origin, []).append(flight)

    # Sort flights by departure time
    for fl in flights_by_origin.values():
        fl.sort(key=lambda f: f.departureTime)

    return FlightData(airports, flights_by_origin)
