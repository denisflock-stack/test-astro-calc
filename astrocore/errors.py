"""Custom error classes for astrocore."""
from __future__ import annotations


class AstroCoreError(Exception):
    """Base class for astrocore errors."""


class InvalidInputError(AstroCoreError):
    """Raised when input data is invalid."""


class EphemerisError(AstroCoreError):
    """Raised when ephemeris files are missing or invalid."""


class CalculationError(AstroCoreError):
    """Raised when a calculation fails."""


__all__ = [
    "AstroCoreError",
    "InvalidInputError",
    "EphemerisError",
    "CalculationError",
]
