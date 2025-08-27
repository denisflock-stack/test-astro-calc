"""Swiss Ephemeris wrapper utilities."""
from __future__ import annotations

import threading
from typing import Dict, Any

import swisseph as swe

from ..config import DEFAULT_EPHE_PATH, AYANAMSA_MAP

_swe_lock = threading.Lock()
_initialized = False


def init_ephemeris(ephe_path: str | None = None, ayanamsa: str = "Lahiri", sidereal: bool = True) -> None:
    """Initialise Swiss Ephemeris library."""
    global _initialized
    with _swe_lock:
        if _initialized:
            return
        swe.set_ephe_path(str(ephe_path or DEFAULT_EPHE_PATH))
        if sidereal:
            swe.set_sid_mode(AYANAMSA_MAP.get(ayanamsa, swe.SIDM_LAHIRI))
        _initialized = True


def calc_ut(jd_ut: float, body: int, flags: int) -> Dict[str, Any]:
    """Thread-safe wrapper around ``swe.calc_ut``."""
    with _swe_lock:
        pos, _ = swe.calc_ut(jd_ut, body, flags)
    return {
        "lon": pos[0],
        "lat": pos[1],
        "dist": pos[2],
        "speed_lon": pos[3],
    }


def houses(jd_ut: float, lat: float, lon: float):
    """Thread-safe wrapper around ``swe.houses``."""
    with _swe_lock:
        return swe.houses(jd_ut, lat, lon)


def get_ayanamsa(jd_ut: float) -> float:
    with _swe_lock:
        return swe.get_ayanamsa(jd_ut)


def sidtime(jd_ut: float) -> float:
    with _swe_lock:
        return swe.sidtime(jd_ut)


def ecl_nut(jd_ut: float):
    with _swe_lock:
        pos, _ = swe.calc_ut(jd_ut, swe.ECL_NUT)
    return pos

