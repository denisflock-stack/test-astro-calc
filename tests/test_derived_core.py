from __future__ import annotations

from typing import Dict
from unittest.mock import patch

from derived.core import build_derived_core


def sample_payload() -> Dict[str, object]:
    return {
        "date": "2000-01-01",
        "time": "12:00",
        "tz_offset_hours": 0.0,
        "latitude_deg": 0.0,
        "longitude_deg": 0.0,
    }


def test_build_derived_core_calls_base_core_once() -> None:
    payload = sample_payload()
    core = {"planets": {}, "houses": {}}
    with (
        patch("derived.core.build_base_core", return_value=core) as mock_base,
        patch("derived.core.compute_aspects", return_value={}),
        patch("derived.core.compute_signs", return_value={}),
    ):
        build_derived_core(payload)
    mock_base.assert_called_once_with(payload)


def test_build_derived_core_passes_core_to_helpers() -> None:
    payload = sample_payload()
    core = {"planets": {"Sun": {"lon_deg": 50.0}}, "houses": {"house_system": "X"}}
    with (
        patch("derived.core.build_base_core", return_value=core),
        patch("derived.core.compute_aspects") as mock_aspects,
        patch("derived.core.compute_signs") as mock_signs,
    ):
        build_derived_core(payload)
    mock_aspects.assert_called_once_with(core)
    mock_signs.assert_called_once_with(core)
