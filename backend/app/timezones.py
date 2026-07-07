"""
Time-zone-aware helpers. Used for every duration computed anywhere in the app
(layover length, total trip duration) via to_utc()
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def to_utc(local_iso: str, tz_name: str) -> datetime:
    """
    Parse ISO datetime into naive, then attach its timezone name
    to be converted to UTC datetime.

    Returns an aware UTC datetime.
    """
    naive = datetime.fromisoformat(local_iso)
    local = naive.replace(tzinfo=ZoneInfo(tz_name))
    return local.astimezone(timezone.utc)


def minutes_between(earlier_utc: datetime, later_utc: datetime) -> int:
    """
    Returns difference in minutes between two times
    """
    delta = later_utc - earlier_utc
    return int(delta.total_seconds() // 60)
