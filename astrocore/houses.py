"""House calculations for astrocore.

The module exposes :func:`compute_houses` which returns a unified contract for
all supported house systems.  The contract is built around three arrays:

``cusps_deg_sid`` – midpoints of houses (bhāva-madhya) in sidereal longitude.
``borders_deg_sid`` – house borders (bhāva-sandhi); optional.
``width_deg`` – widths of houses on the ecliptic; optional.

Every array, when present, has length 12 with index ``0`` corresponding to the
first house.  Values are normalised to ``[0, 360)``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Dict, List

import math

from .constants import (
    ASC_DEG_SID,
    MC_DEG_SID,
    ASC_DEG_TROP,
    MC_DEG_TROP,
    DESC_DEG_SID,
    IC_DEG_SID,
    AYANAMSA_DEG,
    EPSILON_DEG,
    RAMC_DEG,
)
from .eph import swiss
from .eph.base_core import compute_geometry
from .utils.angles import mod360

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------



@dataclass
class HouseRequest:
    jd_ut: float
    geo_lat_deg: float
    geo_lon_deg: float
    ayanamsa: str = "Lahiri"
    house_system: Literal["whole-sign", "sripati", "placidus"] = "whole-sign"
    backend: Literal["auto", "swiss", "native"] = "auto"
    options: Dict[str, object] = field(default_factory=dict)



# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

WSH_EPS = 1e-9


def to_sidereal(lon_trop_deg: float, ayanamsa_deg: float) -> float:
    """Convert a tropical longitude to sidereal using given ayanamsa."""
    return mod360(lon_trop_deg - ayanamsa_deg)


def compute_angles_native(
    jd_ut: float, lat: float, lon: float, epsilon_mode: str = "true-of-date"
) -> Dict[str, float]:
    """Return Ascendant and Midheaven longitudes in the tropical zodiac.

    Uses a Swiss Ephemeris call with the Porphyry system to ensure validity
    across all latitudes without incurring Placidus errors.
    """

    _, ascmc = swiss.houses_ex(jd_ut, lat, lon, b"O")
    return {ASC_DEG_TROP: ascmc[0], MC_DEG_TROP: ascmc[1]}


def compute_sripati_from_angles(asc: float, mc: float) -> List[float]:
    """Compute Śrīpati (Porphyry) house *cusps* from Asc and MC (sidereal).

    Returned array contains midpoints of houses starting from index 0 = house I.
    """


    asc = mod360(asc)
    mc = mod360(mc)
    ic = mod360(mc + 180.0)
    desc = mod360(asc + 180.0)
    cusps = [0.0] * 12
    cusps[0] = asc  # 1st house
    cusps[3] = ic   # 4th house
    cusps[6] = desc # 7th house
    cusps[9] = mc   # 10th house

    arc_mc_asc = (asc - mc) % 360.0
    step1 = arc_mc_asc / 3.0
    cusps[10] = mod360(mc + step1)        # 11th
    cusps[11] = mod360(mc + 2 * step1)    # 12th
    cusps[4] = mod360(cusps[10] + 180.0)  # 5th
    cusps[5] = mod360(cusps[11] + 180.0)  # 6th

    arc_asc_ic = (ic - asc) % 360.0
    step2 = arc_asc_ic / 3.0
    cusps[1] = mod360(asc + step2)        # 2nd
    cusps[2] = mod360(asc + 2 * step2)    # 3rd
    cusps[7] = mod360(cusps[1] + 180.0)   # 8th
    cusps[8] = mod360(cusps[2] + 180.0)   # 9th

    return [mod360(c) for c in cusps]



def widths_from_borders(borders: List[float]) -> List[float]:
    """Compute widths between consecutive borders."""

    return [
        (borders[(i + 1) % 12] - borders[i]) % 360.0
        for i in range(12)
    ]


def madhya_from_borders(borders: List[float]) -> List[float]:
    """Return midpoints (cusps) for given borders."""

    widths = widths_from_borders(borders)
    return [mod360(borders[i] + widths[i] / 2.0) for i in range(12)]


def borders_from_madhya(cusps: List[float]) -> List[float]:
    """Infer borders from cusps midpoints."""

    borders: List[float] = []
    for i in range(12):
        prev = cusps[i - 1]
        cur = cusps[i]
        diff = (cur - prev) % 360.0
        borders.append(mod360(prev + diff / 2.0))
    return borders


def _whole_sign_borders(asc_sid: float) -> List[float]:
    """Internal helper for Whole-sign borders using EPS to handle boundaries."""

    start = math.floor((asc_sid - WSH_EPS) / 30.0) * 30.0
    return [mod360(start + i * 30.0) for i in range(12)]


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def compute_houses(req: HouseRequest) -> Dict[str, object]:
    """Return house data according to :class:`HouseRequest`.

    The result dictionary contains ``meta``, ``angles``, ``houses`` and
    ``classification`` keys.  ``houses`` follow the contract described in the
    module docstring.
    """


    backend = req.backend
    if backend == "auto":
        backend = "native" if req.house_system in ("whole-sign", "sripati") else "swiss"


    options = req.options or {}
    return_borders = bool(options.get("return_borders"))
    return_width = bool(options.get("return_width"))

    status = "ok"
    notes = ""

    ayanamsa_name = req.ayanamsa
    try:
        swiss.set_sid_mode(ayanamsa_name)
    except ValueError:
        ayanamsa_name = "Lahiri"
        status = "warn"
        notes = f"unknown ayanamsa {req.ayanamsa}, fallback to Lahiri"
        swiss.set_sid_mode(ayanamsa_name)

    geometry = compute_geometry(req.jd_ut, req.geo_lat_deg, req.geo_lon_deg)
    ayanamsa_deg = geometry[AYANAMSA_DEG]
    ramc_deg = geometry[RAMC_DEG]
    epsilon_deg = geometry[EPSILON_DEG]

    houses: Dict[str, object] = {}
    angles: Dict[str, float] = {}

    if req.house_system == "placidus" and backend == "swiss":
        try:
            borders_trop, ascmc = swiss.houses_ex(
                req.jd_ut, req.geo_lat_deg, req.geo_lon_deg, b"P"
            )
            asc_trop, mc_trop = ascmc[0], ascmc[1]
            borders_sid = [to_sidereal(b, ayanamsa_deg) for b in borders_trop]
            cusps_sid = madhya_from_borders(borders_sid)

            houses["type"] = "cuspal"
            houses["cusps_deg_sid"] = cusps_sid
            if return_borders:
                houses["borders_deg_sid"] = borders_sid
            if return_width:
                houses["width_deg"] = widths_from_borders(borders_sid)

            angles[ASC_DEG_SID] = to_sidereal(asc_trop, ayanamsa_deg)
            angles[MC_DEG_SID] = to_sidereal(mc_trop, ayanamsa_deg)
        except Exception:
            backend = "native"
            status = "fallback"
            notes = "fallback to sripati because placidus undefined at latitude"

    if not angles:  # Whole-sign or Śrīpати or fallback branch
        ang = compute_angles_native(req.jd_ut, req.geo_lat_deg, req.geo_lon_deg)
        asc_sid = to_sidereal(ang[ASC_DEG_TROP], ayanamsa_deg)
        mc_sid = to_sidereal(ang[MC_DEG_TROP], ayanamsa_deg)
        angles[ASC_DEG_SID] = asc_sid
        angles[MC_DEG_SID] = mc_sid

        if req.house_system == "whole-sign":
            houses["type"] = "sign-based"
            borders = _whole_sign_borders(asc_sid)
            cusps = [mod360(b + 15.0) for b in borders]
            houses["cusps_deg_sid"] = cusps
            houses["madhya_deg_sid"] = cusps[:]  # alias for compatibility
            if return_borders:
                houses["borders_deg_sid"] = borders
            if return_width:
                houses["width_deg"] = [30.0] * 12
        else:  # Śrīpati or placidus fallback
            houses["type"] = "cuspal"
            cusps = compute_sripati_from_angles(asc_sid, mc_sid)
            houses["cusps_deg_sid"] = cusps
            if return_borders or return_width:
                borders = borders_from_madhya(cusps)
                if return_borders:
                    houses["borders_deg_sid"] = borders
                if return_width:
                    houses["width_deg"] = widths_from_borders(borders)

    angles[DESC_DEG_SID] = mod360(angles[ASC_DEG_SID] + 180.0)
    angles[IC_DEG_SID] = mod360(angles[MC_DEG_SID] + 180.0)

    meta = {
        "house_system": req.house_system,
        "backend": backend,
        "ayanamsa_name": ayanamsa_name,
        AYANAMSA_DEG: ayanamsa_deg,
        EPSILON_DEG: epsilon_deg,
        RAMC_DEG: ramc_deg,

        "status": status,
    }
    if notes:
        meta["notes"] = notes

    classification = {
        "kendra": [1, 4, 7, 10],
        "trikona": [1, 5, 9],
        "upachaya": [3, 6, 10, 11],
        "dusthana": [6, 8, 12],
    }

    return {
        "meta": meta,
        "angles": angles,
        "houses": houses,
        "classification": classification,
    }


__all__ = [
    "HouseRequest",
    "compute_houses",
    "compute_sripati_from_angles",
    "compute_angles_native",
    "to_sidereal",
]


