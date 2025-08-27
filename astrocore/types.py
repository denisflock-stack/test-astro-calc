"""Public type hints for astrocore API."""
from __future__ import annotations

from typing import TypedDict, Literal, Dict, Any


class CoreSettings(TypedDict, total=False):
    sidereal: bool
    ayanamsa: str
    node_type: Literal["TRUE", "MEAN"]
    topocentric: bool


class BaseInput(TypedDict):
    date: str
    time: str
    tz_offset_hours: float
    latitude: float
    longitude: float
    settings: CoreSettings


CoreOutput = Dict[str, Any]

__all__ = ["CoreSettings", "BaseInput", "CoreOutput"]
