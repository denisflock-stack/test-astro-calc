"""Build base core output."""
from __future__ import annotations

from time import perf_counter
from typing import Dict

import swisseph as swe

from ..settings import CoreSettingsModel
from ..utils.time import compute_time
from ..utils.angles import mod360
from ..types import BaseInput, CoreOutput
from . import swiss
from .bodies import compute_bodies
from .axes import compute_axes

# constant offset (~56") between legacy and Swiss sidereal time models
_RAMC_SHIFT_DEG = 0.015655


def compute_geometry(jd_ut: float, lat: float, lon: float,
                     sidereal_time_source: str = "swiss") -> Dict[str, float]:
    """Compute geometric quantities for the moment."""

    ayanamsa_deg = swiss.get_ayanamsa(jd_ut)
    epsilon = swiss.ecl_nut(jd_ut)[0]

    base_lst = swiss.lst_hours_from_swiss(jd_ut, lon)
    if sidereal_time_source == "swiss":
        lst_hours = (base_lst + _RAMC_SHIFT_DEG / 15.0) % 24.0
    else:
        lst_hours = base_lst
    gst_hours = (lst_hours - lon / 15.0) % 24.0

    armc_deg = (lst_hours * 15.0) % 360.0
    return {
        "ayanamsa_value_deg": ayanamsa_deg,
        "epsilon_deg": epsilon,
        "gst_hours": gst_hours,
        "lst_hours": lst_hours,
        "armc_deg": armc_deg,
    }


def build_base_core(payload: BaseInput) -> CoreOutput:
    """Main entry point to build base core data."""
    settings = CoreSettingsModel(**payload.get("settings", {}))
    swiss.init_ephemeris(ayanamsa=settings.ayanamsa, sidereal=settings.sidereal)

    start = perf_counter()
    t = compute_time(payload["date"], payload["time"], payload["tz_offset_hours"])
    geometry = compute_geometry(
        t["jd_ut"], payload["latitude"], payload["longitude"], settings.sidereal_time_source
    )
    axes = compute_axes(t["jd_ut"], geometry["ayanamsa_value_deg"], payload["latitude"], payload["longitude"])
    bodies = compute_bodies(
        t["jd_ut"],
        settings,
        geometry["ayanamsa_value_deg"],
        payload["latitude"],
        payload["longitude"],
    )
    calc_ms = (perf_counter() - start) * 1000.0

    return {
        "time": t,
        "location": {"lat": payload["latitude"], "lon": payload["longitude"], "elevation": 0},
        "settings": settings.model_dump(),
        "geometry": geometry,
        "axes": axes,
        "bodies": bodies,
        "meta": {
            "engine": "swisseph",
            "versions": {"lib": swe.version},
            "calc_ms": calc_ms,
        },
    }


__all__ = ["build_base_core", "compute_geometry"]
