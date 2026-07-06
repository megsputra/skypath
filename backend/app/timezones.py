"""
Time-zone-aware helpers. Every duration computed anywhere in the app
(layover length, total trip duration) must go through to_utc() first --
comparing the local-time strings directly across two different airports'
timezones gives wrong answers, and silently so.
"""

from datetime import datetime
from zoneinfo import ZoneInfo


def to_utc(local_iso: str, tz_name: str) -> datetime:
    """
    Step 1.

    TODO:
    Parse `local_iso` (e.g. "2024-03-15T08:30:00") as a naive datetime,
    attach `tz_name` (a zoneinfo name, e.g. "America/New_York") as its
    timezone using zoneinfo.ZoneInfo, then convert to UTC.
    Return an aware UTC datetime.
    """
    naive = datetime.fromisoformat(local_iso)
    local = naive.replace(tzinfo=ZoneInfo(tz_name))
    return local.astimezone(timezone.utc)


def is_domestic(country_a: str, country_b: str) -> bool:
    """Step 1. True if a connection between these two countries counts as domestic."""
    return country_a == country_b


def minutes_between(earlier_utc: datetime, later_utc: datetime) -> int:
    """
    Step 1.

    TODO: whole minutes from `earlier_utc` to `later_utc`. Used for both
    layover length and total itinerary duration -- keep it in one place
    so rounding/truncation behavior is consistent everywhere.
    """
    delta = later_utc - earlier_utc
    return int(delta.total_seconds() // 60)
