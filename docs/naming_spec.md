# Naming Specification

This project follows a uniform naming scheme for public APIs and internal code.

## Normative

- Use **snake_case** for all identifiers.
- Geographic coordinates: `latitude_deg`, `longitude_deg`.
- Time zone offsets: `tz_offset_hours`.
- Planets expose:
  - `lon_tropical_deg`, `lat_tropical_deg`
  - `lon_sidereal_deg`
  - `distance_au`
  - `speed_lon_deg_per_day`
- Axes keys: `asc_deg_trop`, `mc_deg_trop`, `asc_deg_sid`, `mc_deg_sid`.
- Houses: `house_system`, `cusps_deg_sid` (exactly 12 values).
- Nodes: `settings.node_type` ∈ {`TRUE`, `MEAN`}; data keys `Rahu.lon_sidereal_deg`, `Ketu.lon_sidereal_deg`.

## Examples

```json
{
  "time": {"tz_offset_hours": 4.0},
  "location": {"latitude_deg": 44.7, "longitude_deg": 43.0},
  "axes": {"asc_deg_sid": 12.3, "mc_deg_sid": 102.4}
}
```

## Forbidden aliases and typos

The following legacy names are not allowed and are checked by pre-commit:

- `lat`, `lon` (as coordinate fields)
- `tz_offset`
- `lon_trop_deg`
- `madhya_deg_sid`
- `Śrīpати` (mixed alphabet typo)
