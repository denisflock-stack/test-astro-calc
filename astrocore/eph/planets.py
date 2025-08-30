"""Compute positions of celestial planets."""
from __future__ import annotations

from typing import Dict

import swisseph as swe

from ..settings import CoreSettingsModel
from ..utils.angles import mod360
from . import swiss

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}


def compute_planets(
    jd_ut: float,
    settings: CoreSettingsModel,
    ayanamsa_deg: float,
    latitude_deg: float,
    longitude_deg: float,
) -> Dict[str, Dict[str, float]]:
    """Compute planetary positions."""
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    # if settings.sidereal:
    #     flags |= swe.FLG_SIDEREAL
    if settings.topocentric:
        swe.set_topo(longitude_deg, latitude_deg, 0)
        flags |= swe.FLG_TOPOCTR

    result: Dict[str, Dict[str, float]] = {}
    for name, code in PLANETS.items():
        data = swiss.calc_ut(jd_ut, code, flags)
        result[name] = {
            "lon_tropical_deg": data["lon_deg"],
            "lat_tropical_deg": data["lat_deg"],
            "distance_au": data["distance_au"],
            "speed_lon_deg_per_day": data["speed_lon_deg_per_day"],
            "lon_sidereal_deg": mod360(data["lon_deg"] - ayanamsa_deg),
        }

    for node_name, node_code in ("TrueNode", swe.TRUE_NODE), ("MeanNode", swe.MEAN_NODE):
        data = swiss.calc_ut(jd_ut, node_code, flags)
        result[node_name] = {
            "lon_tropical_deg": data["lon_deg"],
            "lon_sidereal_deg": mod360(data["lon_deg"] - ayanamsa_deg),
        }

    node_key = "TrueNode" if settings.node_type == "TRUE" else "MeanNode"
    rahu_lon = result[node_key]["lon_sidereal_deg"]
    result["Rahu"] = {"lon_sidereal_deg": rahu_lon}
    result["Ketu"] = {"lon_sidereal_deg": mod360(rahu_lon + 180.0)}
    return result


__all__ = ["compute_planets"]
