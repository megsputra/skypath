from datetime import datetime, timezone

from app.timezones import minutes_between, to_utc


def test_to_utc_jfk_departure():
    # By 2024-03-15, US clocks are already in daylight time (DST started
    # March 10), so America/New_York is UTC-4, not UTC-5.
    result = to_utc("2024-03-15T08:30:00", "America/New_York")
    assert result == datetime(2024, 3, 15, 12, 30, tzinfo=timezone.utc)


def test_to_utc_lax_arrival():
    # America/Los_Angeles is UTC-7 in March (also daylight time).
    result = to_utc("2024-03-15T11:45:00", "America/Los_Angeles")
    assert result == datetime(2024, 3, 15, 18, 45, tzinfo=timezone.utc)


def test_to_utc_result_is_aware():
    result = to_utc("2024-03-15T08:30:00", "America/New_York")
    assert result.tzinfo is not None


def test_to_utc_handles_date_line_crossing():
    # SYD is UTC+11 in March. A flight departing SYD late at night local
    # time should still convert to a sane, unambiguous UTC instant.
    result = to_utc("2024-03-15T23:00:00", "Australia/Sydney")
    assert result == datetime(2024, 3, 15, 12, 0, tzinfo=timezone.utc)


def test_minutes_between():
    earlier = datetime(2024, 3, 15, 12, 30, tzinfo=timezone.utc)
    later = datetime(2024, 3, 15, 18, 45, tzinfo=timezone.utc)
    assert minutes_between(earlier, later) == 375  # 6h15m, matches the JFK->LAX example
