# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2026-09-28

### Added

- Added support for 6 new MoSPI datasets:
  - NSS71 Health in India (NSS 71st Round)
  - NSS71E Education in India (NSS 71st Round)
  - NSS72 (72nd Round: Household Expenditure on Services and Durable Goods)
  - NSS72T (72nd Round: Domestic Tourism in India)
  - NSS74 (74th Round: Services Sector Enterprises)
- Added indicator, metadata, and data retrieval support for all newly introduced datasets.
- Added Swagger-based parameter validation for the new datasets.
- Total supported datasets: 36.

### Changed

- Updated NAS support to accept `account_code` (1 or 2) when retrieving indicators and metadata.
- Updated the NAS Swagger specification to include `account_code` and current base-year and series options.

## [0.1.4] - 2026-07-31

### Added

- Added support for 8 new MoSPI datasets:
  - NSS73 (73rd Round - Unincorporated Non-Agricultural Enterprises)
  - NSS75 (75th Round - Household Social Consumption: Health)
  - NSS75E (75th Round - Household Social Consumption: Education)
  - NSS76 (76th Round - Persons with Disabilities)
  - NSS76C (76th Round - Drinking Water, Sanitation, Hygiene and Housing Conditions)
  - NSS80 (80th Round - Comprehensive Annual Modular Survey)
  - NSS80C (80th Round - Household Consumption Expenditure Survey)
  - ISP (Index of Services Production - Trial Series)
- Added indicator, metadata, and data retrieval support for all newly introduced datasets.
- Added static indicator support for ISP (Yearly and Monthly frequencies).
- Added Swagger-based parameter validation for all newly supported datasets.
- Added documentation, examples, and Jupyter notebook coverage for the new datasets.
- Total supported datasets: 30.

### Fixed

- Improved metadata handling for NSS75, NSS75E, NSS76, NSS76C, NSS80, and NSS80C using survey-specific APIs.
- Standardized indicator responses across newly added datasets.
- Improved validation and error handling for newly supported APIs.
- Added comprehensive unit tests covering indicators, metadata, data retrieval, and dataset listing for the new datasets.

### Changed

- Extended the 4-step workflow (`list_datasets` → `get_indicators` → `get_metadata` → `get_data`) to support all newly added datasets.
- Updated dataset registry, aliases, API mappings, Swagger specifications, and validation logic to include the latest datasets.


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
