# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2026-04-30

### Added

- MNRE (Renewable Energy) dataset - state-wise monthly installed capacity for solar, wind, hydro, bio, and total renewable power in MW from the Ministry of New and Renewable Energy.
- Total supported datasets: 22.

## [0.1.2] - 2026-04-08

### Added

- NSS79 (NSS 79th Round) dataset - education, health, digital literacy (CAMS/AYUSH surveys).
- UDISE (Unified District Information System) dataset - school education statistics.
- Total supported datasets: 21.

### Fixed

- WPI `get_metadata` hang caused by cartesian product explosion on large filter responses.
- NSS78 `get_data` now resolves indicator codes to names dynamically (API expects string names).
- NAS `get_indicators` no longer raises false `NoDataError` when API returns misleading message field.
- SSL legacy renegotiation support for newer OpenSSL versions.
- Stripped `viz` and `viz_status` fields from all API responses.

### Changed

- Standardized public error handling so invalid inputs raise `Invalid*` exceptions, no-result queries raise `NoDataError`, and upstream failures raise `APIError`.
- Fixed `list_datasets(format="df")` and `list_datasets(format="csv")`.
- Prevented dataframe/CSV formatting from silently hiding API errors and no-data responses.
- Hardened the tutorial notebook so unstable live endpoints do not crash the full walkthrough.
- Added non-network contract tests, pytest markers, and CI build/test automation.
- Added local build verification to the dev workflow.

## [0.1.0] - 2026-03-24

### Added

- Initial release with 4-step workflow: `list_datasets`, `get_indicators`, `get_metadata`, `get_data`.
- Support for 19 MoSPI datasets: PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, AISHE, ASUSE, GENDER, NFHS, ENVSTATS, RBI, NSS77, NSS78, CPIALRL, HCES, TUS, EC.
- Swagger-based parameter validation for all datasets.
- Indicator enrichment with definitions from JSON files.
- Output format support: `dict`, `df` (pandas DataFrame), `csv`.
- Auto-routing for CPI (Group/Item), IIP (Annual/Monthly), and EC (ranking/detail).
- Retry logic with exponential backoff for transient API failures.
- Custom exceptions: `InvalidDatasetError`, `InvalidFilterError`, `APIError`.
