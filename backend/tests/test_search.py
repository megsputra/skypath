"""
Unit tests for the connection-search logic
"""

from app.data import Airport, Flight, FlightData
from app.search import find_itineraries, is_domestic


def make_airport(code, country="US", tz="UTC"):
    return Airport(code=code, name=code, city=code, country=country, timezone=tz)


def make_flight(number, origin, destination, dep, arr, price=100.0):
    return Flight(
        flightNumber=number,
        airline="Test Air",
        origin=origin,
        destination=destination,
        departureTime=dep,
        arrivalTime=arr,
        price=price,
        aircraft="A320",
    )


def make_data(airports, flights):
    by_origin = {}
    for f in flights:
        by_origin.setdefault(f.origin, []).append(f)
    for lst in by_origin.values():
        lst.sort(key=lambda f: f.departureTime)
    return FlightData(
        airports={a.code: a for a in airports}, flights_by_origin=by_origin
    )


def test_is_domestic_same_country():
    assert is_domestic("US", "US") is True


def test_is_domestic_different_country():
    assert is_domestic("US", "GB") is False


def test_direct_flight_is_found():
    airports = [make_airport("AAA"), make_airport("BBB")]
    flight = make_flight(
        "F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T10:00:00"
    )
    data = make_data(airports, [flight])

    results = find_itineraries(data, "AAA", "BBB", "2024-03-15")

    assert [flight] in results


def test_first_segment_must_depart_on_requested_date():
    airports = [make_airport("AAA"), make_airport("BBB")]
    flight = make_flight(
        "F1", "AAA", "BBB", "2024-03-16T08:00:00", "2024-03-16T10:00:00"
    )
    data = make_data(airports, [flight])

    results = find_itineraries(data, "AAA", "BBB", "2024-03-15")

    assert results == []


def test_domestic_layover_at_45_minutes_is_included():
    airports = [
        make_airport("AAA", "US"),
        make_airport("BBB", "US"),
        make_airport("CCC", "US"),
    ]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "CCC", "2024-03-15T09:45:00", "2024-03-15T11:00:00"
    )  # exactly 45 min
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2] in results


def test_domestic_layover_below_45_minutes_is_excluded():
    airports = [
        make_airport("AAA", "US"),
        make_airport("BBB", "US"),
        make_airport("CCC", "US"),
    ]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "CCC", "2024-03-15T09:30:00", "2024-03-15T11:00:00"
    )  # 30 min, too short
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2] not in results


def test_international_layover_below_90_minutes_is_excluded():
    airports = [
        make_airport("AAA", "US"),
        make_airport("BBB", "US"),
        make_airport("CCC", "GB"),
    ]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "CCC", "2024-03-15T10:00:00", "2024-03-15T13:00:00"
    )  # 60 min, too short
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2] not in results


def test_international_layover_at_90_minutes_is_included():
    airports = [
        make_airport("AAA", "US"),
        make_airport("BBB", "US"),
        make_airport("CCC", "GB"),
    ]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "CCC", "2024-03-15T10:30:00", "2024-03-15T13:00:00"
    )  # exactly 90 min
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2] in results


def test_layover_over_6_hours_is_excluded():
    airports = [make_airport("AAA"), make_airport("BBB"), make_airport("CCC")]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "CCC", "2024-03-15T15:01:00", "2024-03-15T17:00:00"
    )  # 6h1m layover
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2] not in results


def test_layover_at_exactly_6_hours_is_included():
    airports = [make_airport("AAA"), make_airport("BBB"), make_airport("CCC")]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "CCC", "2024-03-15T15:00:00", "2024-03-15T17:00:00"
    )  # 6h0m layover
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2] in results


def test_no_airport_change_during_layover():
    # A flight arrives at JFK; the only onward flight departs from LGA, a
    # different (if nearby) airport. That must NOT be treated as a valid
    # connection, even though the timing would otherwise work.
    airports = [
        make_airport("AAA"),
        make_airport("JFK"),
        make_airport("LGA"),
        make_airport("LAX"),
    ]
    f1 = make_flight("F1", "AAA", "JFK", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight("F2", "LGA", "LAX", "2024-03-15T09:45:00", "2024-03-15T11:00:00")
    data = make_data(airports, [f1, f2])

    results = find_itineraries(data, "AAA", "LAX", "2024-03-15")

    assert results == []


def test_does_not_revisit_an_airport():
    airports = [make_airport("AAA"), make_airport("BBB"), make_airport("CCC")]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T08:00:00", "2024-03-15T09:00:00")
    f2 = make_flight(
        "F2", "BBB", "AAA", "2024-03-15T09:45:00", "2024-03-15T10:45:00"
    )  # back to AAA
    f3 = make_flight("F3", "AAA", "CCC", "2024-03-15T11:30:00", "2024-03-15T12:30:00")
    data = make_data(airports, [f1, f2, f3])

    results = find_itineraries(data, "AAA", "CCC", "2024-03-15")

    assert [f1, f2, f3] not in results


def test_caps_at_three_segments():
    airports = [make_airport(c) for c in ["AAA", "BBB", "CCC", "DDD", "EEE"]]
    f1 = make_flight("F1", "AAA", "BBB", "2024-03-15T06:00:00", "2024-03-15T07:00:00")
    f2 = make_flight("F2", "BBB", "CCC", "2024-03-15T07:45:00", "2024-03-15T08:45:00")
    f3 = make_flight("F3", "CCC", "DDD", "2024-03-15T09:30:00", "2024-03-15T10:30:00")
    f4 = make_flight("F4", "DDD", "EEE", "2024-03-15T11:15:00", "2024-03-15T12:15:00")
    data = make_data(airports, [f1, f2, f3, f4])

    results = find_itineraries(data, "AAA", "EEE", "2024-03-15")

    # Reaching EEE would require 4 segments / 3 connections -- over the cap.
    assert results == []
