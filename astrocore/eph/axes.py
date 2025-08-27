"""Compute ascendant and midheaven axes."""
from __future__ import annotations

from typing import Dict

from ..utils.angles import mod360
from . import swiss


def compute_axes(jd_ut: float, ayanamsa_deg: float, lat: float, lon: float) -> Dict[str, float]:
    """Compute Ascendant and Midheaven."""
    cusps, ascmc = swiss.houses(jd_ut, lat, lon)
    asc_trop = ascmc[0]
    mc_trop = ascmc[1]
    return {
        "asc_tropical_lon_deg": asc_trop,
        "mc_tropical_lon_deg": mc_trop,
        "asc_sidereal_lon_deg": mod360(asc_trop - ayanamsa_deg),
        "mc_sidereal_lon_deg": mod360(mc_trop - ayanamsa_deg),
    }
