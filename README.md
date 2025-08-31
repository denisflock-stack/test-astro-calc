# astrocore

Minimal astrological core calculations using Swiss Ephemeris.

## Houses

`astrocore.houses.compute_houses` returns house cusps, borders and widths in a
unified structure for Whole-sign, Śrīpati and Placidus systems.  All longitudes
are sidereal and normalised to `[0, 360)`.

Ascendant and Midheaven axes are exposed in both sidereal and tropical
longitudes using the keys `asc_deg_sid`, `mc_deg_sid`, `asc_deg_trop`, and
`mc_deg_trop`. Metadata also includes the right ascension of the Midheaven
as `ramc_deg`.

## Example

```python
from astrocore import build_base_core

payload = {
    "date": "2024-01-01",
    "time": "12:00",
    "tz_offset_hours": 1.0,
    "latitude_deg": 52.37,
    "longitude_deg": 4.90,
    "settings": {
        "sidereal": True,
        "ayanamsa": "Lahiri",
        "node_type": "MEAN",
        "topocentric": False,
    },
}
result = build_base_core(payload)
print(result["axes"]["asc_deg_sid"], result["axes"]["mc_deg_sid"])
print(result["planets"]["Sun"])
```

## Changelog

- Renamed geometry key `armc_deg` to `ramc_deg` and removed the `lst_deg`
  metadata alias from `compute_houses`.
