"""Angle helpers."""
from __future__ import annotations


def mod360(value: float) -> float:
    """Normalize value to 0..360 degrees."""
    return value % 360.0


__all__ = ["mod360"]
