"""Derived core calculations."""
from __future__ import annotations

from typing import Any, Dict

from astrocore import build_base_core
from astrocore.types import BaseInput, CoreOutput

from .signs import lon_to_sign_deg


def compute_aspects(core: CoreOutput) -> Dict[str, Any]:
    """Compute simplistic aspects between planets.

    The implementation is intentionally lightweight: for every unique pair of
    planets it computes the absolute difference in longitude and folds values
    greater than 180 degrees. The house system is also passed through so the
    function touches both planetary and house data from the core payload.
    """
    planets = core.get("planets", {})
    houses = core.get("houses", {})
    names = list(planets.keys())
    aspects: Dict[str, float] = {}
    for i, p1 in enumerate(names):
        lon1 = planets[p1].get("lon_deg") or planets[p1].get("lon_sidereal_deg") or planets[p1].get("lon_tropical_deg")
        if lon1 is None:
            continue
        for p2 in names[i + 1 :]:
            lon2 = planets[p2].get("lon_deg") or planets[p2].get("lon_sidereal_deg") or planets[p2].get("lon_tropical_deg")
            if lon2 is None:
                continue
            diff = abs(lon1 - lon2) % 360.0
            if diff > 180.0:
                diff = 360.0 - diff
            aspects[f"{p1}-{p2}"] = diff
    return {"pairs": aspects, "house_system": houses.get("house_system")}


def compute_signs(core: CoreOutput) -> Dict[str, str]:
    """Map each planet to its zodiac sign."""
    result: Dict[str, str] = {}
    for name, data in core.get("planets", {}).items():
        lon = data.get("lon_sidereal_deg") or data.get("lon_tropical_deg") or data.get("lon_deg")
        if lon is None:
            continue
        sign, _ = lon_to_sign_deg(lon)
        result[name] = sign
    return result


def build_derived_core(payload: BaseInput) -> Dict[str, Any]:
    """Build combined core data with derived calculations."""
    core = build_base_core(payload)
    derived = {
        "aspects": compute_aspects(core),
        "signs": compute_signs(core),
    }
    return {**core, **derived}


__all__ = ["build_derived_core", "compute_aspects", "compute_signs"]
