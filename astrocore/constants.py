"""Shared constant key names for astrocore."""
from __future__ import annotations

# Axis keys
ASC_DEG_SID = "asc_deg_sid"
MC_DEG_SID = "mc_deg_sid"
ASC_DEG_TROP = "asc_deg_trop"
MC_DEG_TROP = "mc_deg_trop"

AXES_KEYS = {
    ASC_DEG_SID,
    MC_DEG_SID,
    ASC_DEG_TROP,
    MC_DEG_TROP,
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
    "AXES_KEYS",
    "AYANAMSA_DEG",
    "EPSILON_DEG",
    "GST_HOURS",
    "LST_HOURS",
    "RAMC_DEG",
    "GEOMETRY_KEYS",
]
