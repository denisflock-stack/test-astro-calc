import math

from astrocore.houses import HouseRequest, compute_houses


REQ_ARGS = dict(
    jd_ut=2447013.856,
    geo_lat_deg=44.7153,
    geo_lon_deg=42.9979,
    ayanamsa="Lahiri",
)


def test_whole_sign_houses_structure():
    req = HouseRequest(
        **REQ_ARGS,
        house_system="whole-sign",
        backend="native",
        options={"return_width": True},
    )
    data = compute_houses(req)

    houses = data["houses"]
    angles = data["angles"]

    assert houses["type"] == "sign-based"
    borders = houses["borders_deg_sid"]
    assert len(borders) == 12
    # first border is start of the ascendant sign
    asc = angles["asc_deg_sid"]
    expected_start = math.floor(asc / 30.0) * 30.0
    assert math.isclose(borders[0], expected_start, abs_tol=1e-6)
    # consecutive borders differ by 30 degrees
    diffs = [
        (borders[(i + 1) % 12] - borders[i]) % 360.0 for i in range(12)
    ]
    assert all(math.isclose(d, 30.0, abs_tol=1e-6) for d in diffs)
    # widths are all 30 degrees
    assert houses["width_deg"] == [30.0] * 12


def test_sripati_cusps_consistency():
    req = HouseRequest(
        **REQ_ARGS,
        house_system="sripati",
        backend="native",
        options={"return_borders": True, "return_width": True},
    )
    data = compute_houses(req)
    houses = data["houses"]
    angles = data["angles"]

    cusps = houses["cusps_deg_sid"]
    assert len(cusps) == 12
    # cusp 1 equals ascendant; cusp 10 equals midheaven
    assert math.isclose(cusps[0], angles["asc_deg_sid"], abs_tol=1e-6)
    assert math.isclose(cusps[9], angles["mc_deg_sid"], abs_tol=1e-6)
    # widths sum to 360 degrees
    assert math.isclose(sum(houses["width_deg"]), 360.0, abs_tol=1e-6)
