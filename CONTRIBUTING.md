# Contributing to nsoindia

Thank you for your interest in contributing! This project aims to make India's public statistical data accessible to every developer and researcher.

## Getting Started

1. **Fork and clone** the repository:

   ```bash
   git clone https://github.com/nso-india/mospidata.git
   cd mospidata
   ```

2. **Create a virtual environment** and install dev dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Run tests** to verify your setup:

   ```bash
   pytest -q -m "not network"
   ```

## Development Workflow

1. Create a new branch from `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests.

3. Run the test suite:

   ```bash
   pytest -q -m "not network"
   pytest -q
   python -m build
   ```

4. Commit with a clear message and open a pull request.

## Project Structure

```
nsoindia/
├── __init__.py          # Public API (list_datasets, get_indicators, get_metadata, get_data)
├── client.py            # HTTP client for all 19 MoSPI dataset APIs
├── datasets.py          # Dataset registry, swagger validation, enrichment
├── exceptions.py        # Custom exceptions
├── formatters.py        # Output format conversions (dict, DataFrame, CSV)
├── swagger/             # 19 OpenAPI YAML specs (validation source of truth)
└── definitions/         # Indicator definition JSON files (enrichment)
```

## Areas for Contribution

- **New datasets** - If MoSPI adds new datasets, add the endpoint to `client.py`, swagger spec to `swagger/`, and routing to `__init__.py`.
- **Better output formatting** - Improve DataFrame column types, add more export formats.
- **Documentation** - Examples, tutorials, Jupyter notebooks.
- **Tests** - Expand test coverage across all 19 datasets.
- **Bug fixes** - If you encounter issues with specific datasets or filters.

## Adding a New Dataset

1. Add the API endpoint to `MoSPI.api_endpoints` in `client.py`.
2. Add `get_{dataset}_indicators()` and `get_{dataset}_filters()` methods to `client.py`.
3. Add the swagger YAML spec to `nsoindia/swagger/`.
4. Add the dataset to `VALID_DATASETS`, `DATASET_SWAGGER`, and `DATASET_DESCRIPTIONS` in `datasets.py`.
5. Add routing in `get_indicators()`, `get_metadata()`, and `get_data()` in `__init__.py`.
6. Add a definitions JSON to `nsoindia/definitions/` if indicator descriptions are available.
7. Add tests.

## Code Style

- Keep it simple - minimal abstractions, no over-engineering.
- Follow existing patterns in the codebase.
- No unnecessary dependencies.
- Preserve the public exception contract:
  - `InvalidDatasetError` for unknown datasets
  - `InvalidFilterError` for invalid/missing local inputs
  - `NoDataError` for valid requests with no matching rows
  - `APIError` for upstream/network failures

## Test Strategy

- `pytest -q -m "not network"` runs fast, deterministic contract tests and should pass in CI without live API access.
- `pytest -q` includes live MoSPI endpoint tests and may occasionally reflect upstream instability.
- If you touch packaging or release flow, also run `python -m build`.

## Reporting Issues

Open an issue on GitHub with:
- What you tried
- What you expected
- What actually happened
- The dataset and filters you used

---

*This project is developed under the Bharat Digital Collaboration initiative.*
