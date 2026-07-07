import pytest
from fastapi import HTTPException

from app.main import search


def test_unknown_origin_returns_404():
    with pytest.raises(HTTPException) as exc_info:
        search(origin="XXX", destination="LAX", date="2024-03-15")
    assert exc_info.value.status_code == 404
    assert "XXX" in exc_info.value.detail


def test_unknown_destination_returns_404():
    with pytest.raises(HTTPException) as exc_info:
        search(origin="JFK", destination="XXX", date="2024-03-15")
    assert exc_info.value.status_code == 404
    assert "XXX" in exc_info.value.detail


def test_same_origin_and_destination_returns_400():
    with pytest.raises(HTTPException) as exc_info:
        search(origin="JFK", destination="JFK", date="2024-03-15")
    assert exc_info.value.status_code == 400


def test_malformed_date_returns_400():
    with pytest.raises(HTTPException) as exc_info:
        search(origin="JFK", destination="LAX", date="not-a-date")
    assert exc_info.value.status_code == 400


def test_lowercase_airport_codes_are_normalized():
    # Should not raise -- lowercase input is upper()'d before validation.
    response = search(origin="jfk", destination="lax", date="2024-03-15")
    assert response.origin == "JFK"
    assert response.destination == "LAX"
