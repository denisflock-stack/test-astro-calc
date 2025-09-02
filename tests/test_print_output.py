"""Emit full base core calculation for manual verification.

This test runs the ``build_base_core`` pipeline with a fixed payload and
prints the resulting dictionary so it can be inspected in the test logs.
The assertion simply ensures the function returned a truthy value, while
the printout provides the complete calculation result.
"""

import json

from astrocore import build_base_core
from astrocore.constants import (
    ASC_DEG_SID,
    MC_DEG_SID,
    ASC_DEG_TROP,
    MC_DEG_TROP,
    AYANAMSA_DEG,
    RAMC_DEG,
)


def test_print_core_output() -> None:
    payload = {
        "date": "1987-08-14",
        "time": "08:30",
        "tz_offset_hours": 4.0,
        "latitude_deg": 44.7153132,
        "longitude_deg": 42.9978716,
        "settings": {
            "sidereal": True,
            "ayanamsa": "Lahiri",
            "node_type": "TRUE",
            "topocentric": False,
        },
    }
    core = build_base_core(payload)
    print(json.dumps(core, indent=2, sort_keys=True))

    # Verify ayanamsa value is exposed with the new key
    assert AYANAMSA_DEG in core["geometry"]
    assert RAMC_DEG in core["geometry"]

    # Ensure unified axis key names are present
    assert set(core["axes"].keys()) == {
        ASC_DEG_SID,
        MC_DEG_SID,
        ASC_DEG_TROP,
        MC_DEG_TROP,
    }

    # Extra formatted output: planetary positions in DMS
    from astrocore.utils import format_dms360
    from derived.signs import lon_to_sign_deg

    def format_sign_dms(lon_deg: float) -> str:
        """Вернёт 'DD° MM′ SS.SSS″ {Sign}' для долгот 0..360, где DMS — внутри знака."""
        sign, deg_in_sign = lon_to_sign_deg(lon_deg)   # deg_in_sign в диапазоне 0..30
        dms = format_dms360(deg_in_sign)               # форматируем 0..30 как DMS
        return f"{dms} {sign}"

    print("\nFormatted positions:")
    for body_name, data in core.get("planets", {}).items():
        trop_str = "-"
        if "lon_tropical_deg" in data:
            trop_str = format_sign_dms(data["lon_tropical_deg"])

        sid_str = "-"
        if "lon_sidereal_deg" in data:
            sid_str = format_sign_dms(data["lon_sidereal_deg"])

        print(f"{body_name:9s} trop={trop_str:30s} sid={sid_str}")

    assert core

