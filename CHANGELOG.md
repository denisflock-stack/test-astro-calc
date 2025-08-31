# Changelog

## Unreleased
- Renamed geometry key `armc_deg` to `ramc_deg` and removed the `lst_deg`
  metadata alias from `compute_houses`.
- Standardized location fields to `latitude_deg` and `longitude_deg` across
  public APIs and documentation.
- Renamed timezone offset field to `tz_offset_hours`.
- Dropped legacy house aliases and unused axis constants.
- Added naming specification and pre-commit check for forbidden aliases.
