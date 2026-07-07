import os

from app.data import load_flight_data

# repo_root/flights.json -- the real dataset, not a fixture, so these tests
# double as a sanity check that loading actually works end to end.
FLIGHTS_JSON = os.path.join(os.path.dirname(__file__), "..", "..", "flights.json")


def test_loads_all_airports():
    data = load_flight_data(FLIGHTS_JSON)
    assert len(data.airports) == 25


def test_jfk_airport_details():
    data = load_flight_data(FLIGHTS_JSON)
    jfk = data.get_airport("JFK")
    assert jfk is not None
    assert jfk.country == "US"
    assert jfk.timezone == "America/New_York"


def test_unknown_airport_returns_none():
    data = load_flight_data(FLIGHTS_JSON)
    assert data.get_airport("ZZZ") is None


def test_flights_indexed_by_origin():
    data = load_flight_data(FLIGHTS_JSON)
    assert "JFK" in data.flights_by_origin
    assert all(f.origin == "JFK" for f in data.flights_by_origin["JFK"])


def test_flights_sorted_by_departure_time():
    data = load_flight_data(FLIGHTS_JSON)
    jfk_flights = data.flights_by_origin.get("JFK", [])
    departure_times = [f.departureTime for f in jfk_flights]
    assert departure_times == sorted(departure_times)
