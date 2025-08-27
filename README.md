# astrocore

Minimal astrological core calculations using Swiss Ephemeris.

## Example

```python
from astrocore import build_base_core

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
result = build_base_core(payload)
print(result["bodies"]["Sun"])
```
