"""Pydantic settings models for astrocore."""
from __future__ import annotations


from pydantic import BaseModel, field_validator

from typing import Literal

from .config import AYANAMSA_MAP


class CoreSettingsModel(BaseModel):
    """Settings for core calculations."""

    sidereal: bool = True
    ayanamsa: str = "Lahiri"
    node_type: Literal["TRUE", "MEAN"] = "TRUE"
    topocentric: bool = False


    @field_validator("ayanamsa")
    def check_ayanamsa(cls, v: str) -> str:  # noqa: D401
        if v not in AYANAMSA_MAP:
            raise ValueError(f"Unsupported ayanamsa: {v}")
        return v


__all__ = ["CoreSettingsModel"]
