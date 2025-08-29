"""Configuration for astrocore package."""
from __future__ import annotations

import os
from pathlib import Path

import swisseph as swe

# Default path to ephemeris files. Can be overridden with EPHE_PATH env var.
DEFAULT_EPHE_PATH = Path(os.environ.get("EPHE_PATH", Path(__file__).resolve().parent.parent / "ephemeris"))

# Mapping of ayanamsa identifiers to Swiss Ephemeris constants
AYANAMSA_MAP = {
    "Lahiri": swe.SIDM_LAHIRI,
    "Krishnamurti": swe.SIDM_KRISHNAMURTI,
}
