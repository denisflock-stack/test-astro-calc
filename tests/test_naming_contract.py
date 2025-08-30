from typing import Dict

import pytest

from astrocore import build_base_core
from astrocore.houses import HouseRequest, compute_houses
from astrocore.utils.time import compute_time


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
    planets = core["bodies"]
    legacy_key = "lon_trop" + "_deg"
    for p in planets.values():
        assert legacy_key not in p


def test_houses_do_not_expose_madhya_alias(sample_payload):
    t = compute_time(
        sample_payload["date"],
        sample_payload["time"],
        sample_payload["tz_offset_hours"],
    )
    req = HouseRequest(
        jd_ut=t["jd_ut"],
        latitude_deg=sample_payload["latitude_deg"],
        longitude_deg=sample_payload["longitude_deg"],
    )
    data = compute_houses(req)
    houses = data["houses"]
    legacy_alias = "madhya" + "_deg_sid"
    assert legacy_alias not in houses
    assert "cusps_deg_sid" in houses
    assert len(houses["cusps_deg_sid"]) == 12


def test_time_offset_key(sample_payload):
    assert "tz_offset_hours" in sample_payload
