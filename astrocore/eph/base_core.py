"""Build base core output."""
from __future__ import annotations

from time import perf_counter
from typing import Dict

import swisseph as swe

from ..settings import CoreSettingsModel
from ..utils.time import compute_time
from ..types import BaseInput, CoreOutput
from ..constants import (
    AYANAMSA_DEG,
    EPSILON_DEG,
    GST_HOURS,
    LST_HOURS,
    RAMC_DEG,
)
from . import swiss
from .bodies import compute_bodies
from .axes import compute_axes


def compute_geometry(
    jd_ut: float, latitude_deg: float, longitude_deg: float
) -> Dict[str, float]:
    """Compute geometric quantities for the moment."""
    ayanamsa_deg = swiss.get_ayanamsa(jd_ut)
    epsilon = swiss.ecl_nut(jd_ut)[0]
    gst_hours = swiss.sidtime(jd_ut)
    lst_hours = (gst_hours + longitude_deg / 15.0) % 24.0
    ramc_deg = (lst_hours * 15.0) % 360.0
    return {
        AYANAMSA_DEG: ayanamsa_deg,
        EPSILON_DEG: epsilon,
        GST_HOURS: gst_hours,
        LST_HOURS: lst_hours,
        RAMC_DEG: ramc_deg,
    }


def build_base_core(payload: BaseInput) -> CoreOutput:
    """Main entry point to build base core data."""
    settings = CoreSettingsModel(**payload.get("settings", {}))
    swiss.init_ephemeris(ayanamsa=settings.ayanamsa, sidereal=settings.sidereal)

    start = perf_counter()
    t = compute_time(payload["date"], payload["time"], payload["tz_offset_hours"])
    geometry = compute_geometry(
        t["jd_ut"], payload["latitude_deg"], payload["longitude_deg"]
    )
    axes = compute_axes(
        t["jd_ut"],
        geometry[AYANAMSA_DEG],
        payload["latitude_deg"],
        payload["longitude_deg"],
    )  # keys: asc_deg_sid, mc_deg_sid, asc_deg_trop, mc_deg_trop
    bodies = compute_bodies(
        t["jd_ut"],
        settings,
        geometry[AYANAMSA_DEG],
        payload["latitude_deg"],
        payload["longitude_deg"],
    )
    calc_ms = (perf_counter() - start) * 1000.0

    return {
        "time": t,
        "location": {
            "latitude_deg": payload["latitude_deg"],
            "longitude_deg": payload["longitude_deg"],
        },
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
