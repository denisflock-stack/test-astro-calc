
"""Tests for house computations."""

import json
import math

from astrocore.houses import (
    HouseRequest,
    compute_houses,
    _whole_sign_borders,
)



REQ_ARGS = dict(
    jd_ut=2447021.6875,
    geo_lat_deg=44.7153132,
    geo_lon_deg=42.9978716,

)


def test_whole_sign_eps_boundary():
    borders = _whole_sign_borders(30.0 + 1e-8)
    assert math.isclose(borders[0], 30.0, abs_tol=1e-12)
    borders = _whole_sign_borders(30.0)
    assert math.isclose(borders[0], 0.0, abs_tol=1e-12)


def test_whole_sign_structure():
    req = HouseRequest(
        **REQ_ARGS,
        house_system="whole-sign",
        options={"return_borders": True, "return_width": True},

    )
    data = compute_houses(req)
    print("Whole-sign houses output:\n" + json.dumps(data, indent=2, sort_keys=True))

    houses = data["houses"]

    axes = data["axes"]


    assert houses["type"] == "sign-based"
    borders = houses["borders_deg_sid"]

    cusps = houses["cusps_deg_sid"]
    assert len(borders) == len(cusps) == 12

    expected_start = math.floor((axes["asc_deg_sid"] - 1e-9) / 30.0) * 30.0
    assert math.isclose(borders[0], expected_start, abs_tol=1e-6)

    # cusps are borders + 15° and widths are all 30°
    for b, c in zip(borders, cusps):
        assert math.isclose(c, (b + 15.0) % 360.0, abs_tol=1e-6)
    assert houses["width_deg"] == [30.0] * 12


def test_sripati_consistency():
    req = HouseRequest(
        **REQ_ARGS,
        house_system="sripati",

        options={"return_borders": True, "return_width": True},
    )
    data = compute_houses(req)
    print("Śrīpati houses output:\n" + json.dumps(data, indent=2, sort_keys=True))

    houses = data["houses"]
    axes = data["axes"]

    cusps = houses["cusps_deg_sid"]

    borders = houses["borders_deg_sid"]
    widths = houses["width_deg"]
    assert len(cusps) == len(borders) == len(widths) == 12

    assert math.isclose(cusps[0], axes["asc_deg_sid"], abs_tol=1e-6)
    assert math.isclose(cusps[9], axes["mc_deg_sid"], abs_tol=1e-6)

    for i in range(12):
        mid = (cusps[i - 1] + ((cusps[i] - cusps[i - 1]) % 360.0) / 2.0) % 360.0
        assert math.isclose(borders[i], mid, abs_tol=1e-6)
        expected_width = (borders[(i + 1) % 12] - borders[i]) % 360.0
        assert math.isclose(widths[i], expected_width, abs_tol=1e-6)

    assert math.isclose(sum(widths), 360.0, abs_tol=1e-6)


def test_placidus_contract():
    req = HouseRequest(
        **REQ_ARGS,
        house_system="placidus",
        backend="swiss",
        options={"return_borders": True, "return_width": True},
    )
    data = compute_houses(req)
    houses = data["houses"]
    axes = data["axes"]

    borders = houses["borders_deg_sid"]
    cusps = houses["cusps_deg_sid"]
    widths = houses["width_deg"]

    assert math.isclose(borders[0], axes["asc_deg_sid"], abs_tol=1e-6)
    assert math.isclose(borders[9], axes["mc_deg_sid"], abs_tol=1e-6)

    for i in range(12):
        mid = (borders[i] + ((borders[(i + 1) % 12] - borders[i]) % 360.0) / 2.0) % 360.0
        assert math.isclose(cusps[i], mid, abs_tol=1e-6)
        expected_width = (borders[(i + 1) % 12] - borders[i]) % 360.0
        assert math.isclose(widths[i], expected_width, abs_tol=1e-6)

    assert math.isclose(sum(widths), 360.0, abs_tol=1e-6)


def test_placidus_fallback_high_latitude():
    req = HouseRequest(
        jd_ut=2447013.856,
        geo_lat_deg=70.0,
        geo_lon_deg=0.0,
        ayanamsa="Lahiri",
        house_system="placidus",
    )
    data = compute_houses(req)
    meta = data["meta"]
    assert meta["status"] == "fallback"
    assert "placidus undefined" in meta["notes"]


def test_ayanamsa_switch_changes_values():
    req1 = HouseRequest(**REQ_ARGS, ayanamsa="Lahiri")
    req2 = HouseRequest(**REQ_ARGS, ayanamsa="Krishnamurti")

    data1 = compute_houses(req1)
    data2 = compute_houses(req2)

    val1 = data1["meta"]["ayanamsa_deg"]
    val2 = data2["meta"]["ayanamsa_deg"]
    assert not math.isclose(val1, val2, abs_tol=1e-3)

    asc1 = data1["axes"]["asc_deg_sid"]
    asc2 = data2["axes"]["asc_deg_sid"]
    assert not math.isclose(asc1, asc2, abs_tol=1e-3)


