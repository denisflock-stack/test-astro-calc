from typing import Dict

import pytest

from astrocore import build_base_core


@pytest.fixture
def sample_payload() -> Dict[str, object]:
    return {
        "date": "1987-08-14",
        "time": "08:30",
        "tz_offset_hours": 4.0,
        "latitude_deg": 44.7153132,
        "longitude_deg": 42.9978716,
        "settings": {
            "sidereal": True,
            "ayanamsa": "Lahiri",
            "node_type": "MEAN",
            "topocentric": False,
        },
    }


@pytest.fixture
def core_build_fn():
    return build_base_core


def test_location_keys_are_consistent(core_build_fn, sample_payload):
    core = core_build_fn(sample_payload)
    assert set(core["location"].keys()) == {"latitude_deg", "longitude_deg"}


def test_no_legacy_trop_key_in_planets(core_build_fn, sample_payload):
    core = core_build_fn(sample_payload)
    legacy = "lon_trop" + "_deg"
    for p in core["planets"].values():
        assert legacy not in p


def test_houses_expose_only_cusps(core_build_fn, sample_payload):
    core = core_build_fn(sample_payload)
    houses = core["houses"]
    legacy = "madhya" + "_deg_sid"
    assert legacy not in houses
    assert "cusps_deg_sid" in houses and len(houses["cusps_deg_sid"]) == 12


def test_payload_time_key(sample_payload):
    assert "tz_offset_hours" in sample_payload
