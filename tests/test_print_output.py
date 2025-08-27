"""Emit full base core calculation for manual verification.

This test runs the ``build_base_core`` pipeline with a fixed payload and
prints the resulting dictionary so it can be inspected in the test logs.
The assertion simply ensures the function returned a truthy value, while
the printout provides the complete calculation result.
"""

import json

from astrocore import build_base_core


def test_print_core_output() -> None:
    payload = {
        "date": "1987-08-14",
        "time": "08:30",
        "tz_offset_hours": 4.0,
        "latitude": 44.7153132,
        "longitude": 42.9978716,
        "settings": {
            "sidereal": True,
            "ayanamsa": "Lahiri",
            "node_type": "MEAN",
            "topocentric": False,
        },
    }
    core = build_base_core(payload)
    print(json.dumps(core, indent=2, sort_keys=True))

    # Extra formatted output: planetary positions within zodiac signs
    from derived.signs import lon_to_sign_deg

    print("\nFormatted positions:")
    for body_name, data in core.get("bodies", {}).items():
        trop_str = "-"
        if "lon_tropical_deg" in data:
            sign, deg = lon_to_sign_deg(data["lon_tropical_deg"])
            trop_str = f"{deg:.2f}\u00b0 {sign}"

        sid_str = "-"
        if "lon_sidereal_deg" in data:
            sign_s, deg_s = lon_to_sign_deg(data["lon_sidereal_deg"])
            sid_str = f"{deg_s:.2f}\u00b0 {sign_s}"

        print(f"{body_name:9s} trop={trop_str} sid={sid_str}")

    assert core

