# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- Support for all 19 MoSPI datasets: PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, AISHE, ASUSE, GENDER, NFHS, ENVSTATS, RBI, NSS77, NSS78, CPIALRL, HCES, TUS, EC.
- Swagger-based parameter validation for all datasets.
- Indicator enrichment with definitions from JSON files.
- Output format support: `dict`, `df` (pandas DataFrame), `csv`.
- Auto-routing for CPI (Group/Item), IIP (Annual/Monthly), and EC (ranking/detail).
- Retry logic with exponential backoff for transient API failures.
- Custom exceptions: `InvalidDatasetError`, `InvalidFilterError`, `APIError`.
