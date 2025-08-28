"""House calculations for astrocore."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Dict, List

from .eph import swiss

from .eph.base_core import compute_geometry
from .eph.axes import compute_axes

from .utils.angles import mod360


@dataclass
class HouseRequest:
    jd_ut: float
    geo_lat_deg: float
    geo_lon_deg: float
    ayanamsa: str = "Lahiri"
    house_system: Literal["whole-sign", "sripati", "placidus"] = "whole-sign"
    backend: Literal["auto", "swiss", "native"] = "auto"
    options: Dict[str, object] = field(default_factory=dict)



def compute_sripati_from_angles(asc: float, mc: float) -> List[float]:
    """Compute Śrīpati (Porphyry) house cusps from Asc and MC (sidereal)."""
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


def _borders_and_widths(cusps: List[float]) -> Dict[str, List[float]]:
    borders: List[float] = []
    widths: List[float] = []
    for i in range(12):
        c1 = cusps[i]
        c2 = cusps[(i + 1) % 12]
        width = (c2 - c1) % 360.0
        widths.append(width)
        borders.append(mod360(c1 + width / 2.0))
    return {"borders": borders, "width": widths}


def compute_houses(req: HouseRequest) -> Dict[str, object]:
    """Compute house cusps and related data according to request."""
    # Decide backend: sign-based systems don't require Swiss calls.
    backend = req.backend
    if backend == "auto":
        backend = "native" if req.house_system in ("whole-sign", "sripati") else "swiss"


    geometry = compute_geometry(req.jd_ut, req.geo_lat_deg, req.geo_lon_deg)
    ayan_deg = geometry["ayanamsa_value_deg"]

    axes = compute_axes(
        req.jd_ut, ayan_deg, req.geo_lat_deg, req.geo_lon_deg
    )
    angles = {
        "asc_deg_sid": axes["asc_sidereal_lon_deg"],
        "mc_deg_sid": axes["mc_sidereal_lon_deg"],

    }
    angles["desc_deg_sid"] = mod360(angles["asc_deg_sid"] + 180.0)
    angles["ic_deg_sid"] = mod360(angles["mc_deg_sid"] + 180.0)

    houses: Dict[str, object] = {}
    options = req.options or {}
    status = "ok"
    notes = ""

    if req.house_system == "whole-sign":
        houses["type"] = "sign-based"
        asc_sign_start = int(angles["asc_deg_sid"] // 30) * 30.0
        borders = [mod360(asc_sign_start + i * 30.0) for i in range(12)]
        houses["borders_deg_sid"] = borders
        houses["madhya_deg_sid"] = [mod360(b + 15.0) for b in borders]
        if options.get("return_width"):
            houses["width_deg"] = [30.0] * 12
    else:
        houses["type"] = "cuspal"
        if req.house_system == "sripati" or status == "fallback":
            cusps = compute_sripati_from_angles(angles["asc_deg_sid"], angles["mc_deg_sid"])
        else:  # placidus via Swiss
            try:
                cusps_trop, _ = swiss.houses_ex(req.jd_ut, req.geo_lat_deg, req.geo_lon_deg, b"P")
                cusps = [mod360(c - ayan_deg) for c in cusps_trop]

            except Exception:
                status = "fallback"
                notes = "fallback to sripati because placidus undefined at latitude"
                cusps = compute_sripati_from_angles(angles["asc_deg_sid"], angles["mc_deg_sid"])
        houses["cusps_deg_sid"] = cusps
        if options.get("return_borders") or options.get("return_width"):
            bw = _borders_and_widths(cusps)
            if options.get("return_borders"):
                houses["borders_deg_sid"] = bw["borders"]
            if options.get("return_width"):
                houses["width_deg"] = bw["width"]

    meta = {
        "house_system": req.house_system,
        "backend": backend,
        "ayanamsa": {"name": req.ayanamsa, "value_deg": ayan_deg},
        "lst_hours": geometry["lst_hours"],
        "epsilon_deg": geometry["epsilon_deg"],
        "armc_deg": geometry["armc_deg"],

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

]
