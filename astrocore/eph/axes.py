"""Compute ascendant and midheaven axes."""
from __future__ import annotations

from typing import Dict

from ..constants import (
    ASC_DEG_SID,
    MC_DEG_SID,
    ASC_DEG_TROP,
    MC_DEG_TROP,
)
from ..utils.angles import mod360
from . import swiss


def compute_axes(
    jd_ut: float, ayanamsa_deg: float, latitude_deg: float, longitude_deg: float
) -> Dict[str, float]:
    """Compute Ascendant and Midheaven."""
    cusps, ascmc = swiss.houses(jd_ut, latitude_deg, longitude_deg)
    asc_trop = ascmc[0]
    mc_trop = ascmc[1]
    asc_sid = mod360(asc_trop - ayanamsa_deg)
    mc_sid = mod360(mc_trop - ayanamsa_deg)
    return {
        ASC_DEG_SID: asc_sid,
        MC_DEG_SID: mc_sid,
        ASC_DEG_TROP: asc_trop,
        MC_DEG_TROP: mc_trop,
    }
