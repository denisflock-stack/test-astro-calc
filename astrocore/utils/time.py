"""Time related utilities."""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Dict, Any

import swisseph as swe


def compute_time(date: str, time_str: str, tz_offset: float) -> Dict[str, Any]:
    """Normalize time input and compute Julian dates.

    Args:
        date: Date string in ``YYYY-MM-DD`` format.
        time_str: Time string ``HH:MM`` or ``HH:MM:SS``.
        tz_offset: Offset from UTC in hours.

    Returns:
        Dictionary with local/UTC datetimes and Julian day values.
    """

    dt_local = datetime.fromisoformat(f"{date}T{time_str}")
    tzinfo = timezone(timedelta(hours=tz_offset))
    dt_local = dt_local.replace(tzinfo=tzinfo)
    dt_utc = dt_local.astimezone(timezone.utc)

    ut_hour = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, ut_hour)
    delta_t_days = swe.deltat(jd_ut)
    delta_t_sec = delta_t_days * 86400.0
    jd_tt = jd_ut + delta_t_days

    return {
        "datetime_local": dt_local.isoformat(),
        "datetime_utc": dt_utc.isoformat(),
        "jd_ut": jd_ut,
        "delta_t_sec": delta_t_sec,
        "jd_tt": jd_tt,
    }
