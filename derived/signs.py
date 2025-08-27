"""Zodiac sign utilities."""
from __future__ import annotations

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


def lon_to_sign_deg(lon: float) -> tuple[str, float]:
    """Return sign name and degrees within sign for a longitude.

    Args:
        lon: Longitude in degrees (0..360 range accepted).

    Returns:
        A tuple of (sign_name, degrees_in_sign).
    """
    lon = lon % 360.0
    idx = int(lon // 30.0)
    return SIGNS[idx], lon - idx * 30.0


__all__ = ["lon_to_sign_deg", "SIGNS"]
