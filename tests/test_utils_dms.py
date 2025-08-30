import math

import pytest

from astrocore.utils.dms import dec_to_dms360, format_dms360


def test_basic_case():
    angle = 143.0350530119635
    deg, minute, sec = dec_to_dms360(angle)
    assert deg == 143
    assert minute == 2
    assert sec == pytest.approx(6.191, abs=1e-12)
    assert format_dms360(angle) == "143° 02′ 06.191″"
    reconstructed = deg + minute / 60 + sec / 3600
    assert reconstructed == pytest.approx(angle, abs=1e-6)


@pytest.mark.parametrize(
    "value,expected_str",
    [
        (0.0, "0° 00′ 00.000″"),
        (359.9999996, "0° 00′ 00.000″"),
        (360.0, "0° 00′ 00.000″"),
        (-0.0001, "359° 59′ 59.640″"),
        (720.5, "0° 30′ 00.000″"),
    ],
)
def test_edge_cases(value, expected_str):
    deg, minute, sec = dec_to_dms360(value)
    assert 0 <= deg < 360
    assert 0 <= minute < 60
    assert 0 <= sec < 60
    assert format_dms360(value) == expected_str


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_invalid_values(value):
    with pytest.raises(ValueError):
        dec_to_dms360(value)
