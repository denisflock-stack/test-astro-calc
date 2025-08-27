from astrocore import build_base_core


def test_build_base_core_structure():
    payload = {
        "date": "2024-01-01",
        "time": "12:00",
        "tz_offset_hours": 1.0,
        "latitude": 52.37,
        "longitude": 4.90,
        "settings": {
            "sidereal": True,
            "ayanamsa": "Lahiri",
            "node_type": "MEAN",
            "topocentric": False,
        },
    }
    core = build_base_core(payload)
    assert "Sun" in core["bodies"]
    assert "asc_sidereal_lon_deg" in core["axes"]
