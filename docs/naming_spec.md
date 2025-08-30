# Naming Specification

This project follows a uniform naming scheme for public APIs and internal code.

## Normative

- **snake_case** for all identifiers.
- Geographic coordinates use `latitude_deg` and `longitude_deg`.
- Time zone offsets use `tz_offset_hours`.
- Planetary longitudes and latitudes:
  - `lon_tropical_deg`, `lat_tropical_deg`
  - `lon_sidereal_deg`
  - `distance_au`
  - `speed_lon_deg_per_day`
- Axes keys: `asc_deg_trop`, `mc_deg_trop`, `asc_deg_sid`, `mc_deg_sid`.
- House data: `house_system`, `cusps_deg_sid`, optional `borders_deg_sid`, optional `width_deg`.

## Examples

```json
{
  "time": {"tz_offset_hours": 4.0},
  "location": {"latitude_deg": 44.7, "longitude_deg": 43.0},
  "axes": {"asc_deg_sid": 12.3, "mc_deg_sid": 102.4}
}
```

## Forbidden aliases

The following legacy names are not allowed and are checked by pre-commit:

- `tz_offset`
- `lon_trop_deg`
- `madhya_deg_sid`
