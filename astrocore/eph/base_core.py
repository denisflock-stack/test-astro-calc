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


def compute_geometry(jd_ut: float, lat: float, lon: float) -> Dict[str, float]:
    """Compute geometric quantities for the moment."""
    ayanamsa_deg = swiss.get_ayanamsa(jd_ut)
    epsilon = swiss.ecl_nut(jd_ut)[0]
    gst_hours = swiss.sidtime(jd_ut)
    lst_hours = (gst_hours + lon / 15.0) % 24.0
    armc_deg = (lst_hours * 15.0) % 360.0
    return {
        "ayanamsa_deg": ayanamsa_deg,
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
    geometry = compute_geometry(t["jd_ut"], payload["latitude"], payload["longitude"])
    axes = compute_axes(
        t["jd_ut"], geometry["ayanamsa_deg"], payload["latitude"], payload["longitude"]
    )  # keys: asc_deg_sid, mc_deg_sid, asc_deg_trop, mc_deg_trop
    bodies = compute_bodies(
        t["jd_ut"],
        settings,
        geometry["ayanamsa_deg"],
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
