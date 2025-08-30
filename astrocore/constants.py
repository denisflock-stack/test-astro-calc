"""Shared constant key names for astrocore."""
from __future__ import annotations

# Axis keys
ASC_DEG_SID = "asc_deg_sid"
MC_DEG_SID = "mc_deg_sid"
ASC_DEG_TROP = "asc_deg_trop"
MC_DEG_TROP = "mc_deg_trop"
DESC_DEG_SID = "desc_deg_sid"
IC_DEG_SID = "ic_deg_sid"

AXES_KEYS = {
    ASC_DEG_SID,
    MC_DEG_SID,
    ASC_DEG_TROP,
    MC_DEG_TROP,
    DESC_DEG_SID,
    IC_DEG_SID,
}

# Geometry keys
AYANAMSA_DEG = "ayanamsa_deg"
EPSILON_DEG = "epsilon_deg"
GST_HOURS = "gst_hours"
LST_HOURS = "lst_hours"
RAMC_DEG = "ramc_deg"

GEOMETRY_KEYS = {
    AYANAMSA_DEG,
    EPSILON_DEG,
    GST_HOURS,
    LST_HOURS,
    RAMC_DEG,
}

__all__ = [
    "ASC_DEG_SID",
    "MC_DEG_SID",
    "ASC_DEG_TROP",
    "MC_DEG_TROP",
    "DESC_DEG_SID",
    "IC_DEG_SID",
    "AXES_KEYS",
    "AYANAMSA_DEG",
    "EPSILON_DEG",
    "GST_HOURS",
    "LST_HOURS",
    "RAMC_DEG",
    "GEOMETRY_KEYS",
]
