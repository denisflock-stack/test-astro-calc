from astrocore import build_base_core
from astrocore.constants import AXES_KEYS, GEOMETRY_KEYS


def test_core_key_sets() -> None:
    payload = {
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
    core = build_base_core(payload)

    assert set(core["axes"].keys()) <= AXES_KEYS
    assert set(core["geometry"].keys()) <= GEOMETRY_KEYS
