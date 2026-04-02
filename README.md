<p align="center">
  <h1 align="center">esankhyiki</h1>
  <p align="center">Python client for India's National Statistical Office (NSO/MoSPI) data portal</p>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://pypi.org/project/mospi-esankhyiki/"><img src="https://img.shields.io/badge/pypi-v0.1.0-orange.svg" alt="PyPI"></a>
  <a href="https://github.com/nso-india/mospi-esankhyiki"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

---

Access **500+ statistical indicators** across **19 datasets** covering employment, prices, industry, GDP, health, education, environment, trade, and more - directly from Python.

## Installation

```bash
pip install mospi-esankhyiki
```

## Quick Start

```python
import esankhyiki

# Step 1: Discover available datasets
datasets = esankhyiki.list_datasets()

# Step 2: Get indicators for a dataset
indicators = esankhyiki.get_indicators("PLFS")

# Step 3: Get valid filter values for an indicator
metadata = esankhyiki.get_metadata("PLFS", indicator_code=1, frequency_code=1)

# Step 4: Fetch the data
data = esankhyiki.get_data("PLFS", {
    "indicator_code": 1,
    "frequency_code": 1,
    "year": "2023-24",
    "state_code": 99,
    "gender_code": 3,
    "age_code": 1,
    "sector_code": 3,
})
```

---

## The 4-Step Workflow

The API follows a sequential discovery workflow. Filter codes are dataset-specific - always discover them through the workflow instead of guessing.

```
list_datasets()  ->  get_indicators()  ->  get_metadata()  ->  get_data()
      |                    |                    |                  |
  Find the right      See what's          Get valid          Fetch the
    dataset           measured          filter values       actual data
```

**Why this order matters:** `get_metadata()` returns the exact values (state codes, year strings, gender codes, etc.) that `get_data()` expects. Passing arbitrary values will raise `InvalidFilterError`.

---

## API Reference

### `list_datasets(format="dict")`

Returns an overview of all 19 MoSPI statistical datasets.

```python
datasets = esankhyiki.list_datasets()
datasets_df = esankhyiki.list_datasets(format="df")
```

---

### `get_indicators(dataset, format="dict")`

Returns available indicators for a given dataset.

```python
indicators = esankhyiki.get_indicators("PLFS")
```

**Notes by dataset:**
- **PLFS, ASUSE** - indicators are grouped by `frequency_code` (1=Annual, 2=Quarterly, 3=Monthly for PLFS)
- **CPI** - returns available base years instead of named indicators
- **IIP, WPI** - these datasets have no sub-indicators; call `get_metadata()` directly

---

### `get_metadata(dataset, ..., format="dict")`

Returns valid filter values (states, years, quarters, gender codes, etc.) for a given dataset and indicator. The returned `filter_values` show exactly what values are accepted by `get_data()`.

**Full signature:**

```python
esankhyiki.get_metadata(
    dataset,
    indicator_code=None,        # int - required for most datasets
    base_year=None,             # str - required for CPI, IIP, NAS
    level=None,                 # str - required for CPI ("Group" or "Item")
    frequency=None,             # str - required for IIP ("Annually" or "Monthly")
    classification_year=None,   # str - required for ASI (e.g. "2008")
    frequency_code=None,        # int - required for PLFS and ASUSE (1=Annual, 2=Quarterly)
    series=None,                # str - for CPI and NAS ("Current" or "Back")
    use_of_energy_balance_code=None,  # int - for ENERGY (1=Supply, 2=Consumption)
    sub_indicator_code=None,    # int - for RBI (alternative to indicator_code)
    format="dict",
)
```

**Required params by dataset:**

| Dataset | Required params |
|---------|----------------|
| PLFS | `indicator_code`, `frequency_code` |
| CPI | `base_year`, `level` |
| IIP | `base_year`, `frequency` |
| ASI | `classification_year` |
| NAS | `indicator_code`, `base_year`, `frequency_code` |
| WPI | *(none)* |
| ENERGY | `indicator_code` |
| AISHE | `indicator_code` |
| ASUSE | `indicator_code`, `frequency_code` |
| GENDER | `indicator_code` |
| NFHS | `indicator_code` |
| ENVSTATS | `indicator_code` |
| RBI | `indicator_code` or `sub_indicator_code` |
| NSS77 | `indicator_code` |
| NSS78 | `indicator_code` |
| CPIALRL | `indicator_code` |
| HCES | `indicator_code` |
| TUS | `indicator_code` |
| EC | `indicator_code` (1=EC6, 2=EC5, 3=EC4) |

---

### `get_data(dataset, filters, format="dict")`

Fetches statistical data. Use filter values returned by `get_metadata()`.

```python
data = esankhyiki.get_data("PLFS", {
    "indicator_code": 1,
    "frequency_code": 1,
    "year": "2023-24",
    "state_code": 99,
    "gender_code": 3,
    "age_code": 1,
    "sector_code": 3,
})
```

**Pagination** (where supported):

```python
data = esankhyiki.get_data("PLFS", {
    ...,
    "limit": 50,
    "page": 2,
})
```

---

## Output Formats

All four functions accept a `format` parameter:

| Value | Returns |
|-------|---------|
| `"dict"` (default) | Python dict |
| `"df"` or `"dataframe"` | pandas DataFrame |
| `"csv"` | CSV string |

```python
# Default dict
data = esankhyiki.get_data("PLFS", filters)

# DataFrame
df = esankhyiki.get_data("PLFS", filters, format="df")

# CSV
csv = esankhyiki.get_data("PLFS", filters, format="csv")
```

---

## Datasets

| Dataset | Name | Coverage |
|---------|------|----------|
| **PLFS** | Periodic Labour Force Survey | Jobs, unemployment, wages |
| **CPI** | Consumer Price Index | Retail inflation, price indices |
| **IIP** | Index of Industrial Production | Manufacturing, mining output |
| **ASI** | Annual Survey of Industries | Factory financials, employment |
| **NAS** | National Accounts Statistics | GDP, GVA, national income |
| **WPI** | Wholesale Price Index | Wholesale inflation |
| **ENERGY** | Energy Statistics | Energy production and consumption |
| **AISHE** | Higher Education Survey | Universities, enrolment, GER |
| **ASUSE** | Unincorporated Enterprises | Informal sector, MSMEs |
| **GENDER** | Gender Statistics | 147 indicators across all domains |
| **NFHS** | National Family Health Survey | Health, fertility, mortality |
| **ENVSTATS** | Environment Statistics | Climate, biodiversity, pollution |
| **RBI** | RBI Statistics | Trade, forex, exchange rates |
| **NSS77** | NSS 77th Round | Agricultural households |
| **NSS78** | NSS 78th Round | Living conditions |
| **CPIALRL** | CPI for Rural Labourers | Rural inflation |
| **HCES** | Household Consumption | Spending, poverty, Gini |
| **TUS** | Time Use Survey | Time allocation, unpaid work |
| **EC** | Economic Census | District-wise establishments |

---

## Examples

### Unemployment Rate (PLFS)

```python
import esankhyiki

# Discover valid filter values first
meta = esankhyiki.get_metadata("PLFS", indicator_code=3, frequency_code=1)

df = esankhyiki.get_data("PLFS", {
    "indicator_code": 3,      # Unemployment Rate
    "frequency_code": 1,      # Annual
    "year": "2023-24",
    "state_code": 99,         # All India
    "gender_code": 3,         # Person (all genders combined)
    "age_code": 1,
    "sector_code": 3,         # Rural + Urban combined
}, format="df")
```

### GDP / National Accounts (NAS)

```python
meta = esankhyiki.get_metadata(
    "NAS",
    indicator_code=1,
    base_year="2022-23",
    frequency_code=1,
    series="Current",
)

df = esankhyiki.get_data("NAS", {
    "indicator_code": 1,
    "base_year": "2022-23",
    "series": "Current",
    "frequency_code": 1,
}, format="df")
```

### Consumer Price Index (CPI)

```python
# CPI is auto-routed: pass level="Group" for group-level, level="Item" for item-level
meta = esankhyiki.get_metadata("CPI", base_year="2024", level="Group", series="Current")

df = esankhyiki.get_data("CPI", {
    "base_year": "2024",
    "year": "2026",
    "series": "Current",
}, format="df")
```

### Industrial Production (IIP)

```python
# IIP is auto-routed: annual if no month_code, monthly if month_code is present
meta = esankhyiki.get_metadata("IIP", base_year="2011-12", frequency="Annually")

df = esankhyiki.get_data("IIP", {
    "base_year": "2011-12",
    "financial_year": "2023-24",
}, format="df")
```

### Wholesale Price Index (WPI)

```python
# WPI requires no indicator_code
meta = esankhyiki.get_metadata("WPI")

df = esankhyiki.get_data("WPI", {
    "base_year": "2011-12",
    "year": "2023-24",
    "series": "All Commodities",
}, format="df")
```

### Annual Survey of Industries (ASI)

```python
meta = esankhyiki.get_metadata("ASI", classification_year="2008")

df = esankhyiki.get_data("ASI", {
    "classification_year": "2008",
    "indicator_code": 1,
    "year": "2021-22",
}, format="df")
```

### Economic Census (District-wise, EC)

The EC dataset has two modes: **ranking** (top/bottom N districts) and **detail** (row-level records).

```python
# Check available filters
meta = esankhyiki.get_metadata("EC", indicator_code=1)  # EC6 (2013-14)

# Ranking mode - top 5 districts in Assam by establishments
data = esankhyiki.get_data("EC", {
    "indicator_code": 1,      # EC6
    "state": "18",            # Assam
    "mode": "ranking",
    "top5opt": "2",           # Top 5
})

# Detail mode - paginated row-level data (20 rows per page)
data = esankhyiki.get_data("EC", {
    "indicator_code": 1,
    "state": "18",
    "mode": "detail",
    "pageNum": "1",
})
```

### Gender Statistics

```python
indicators = esankhyiki.get_indicators("GENDER")
meta = esankhyiki.get_metadata("GENDER", indicator_code=1)

df = esankhyiki.get_data("GENDER", {
    "indicator_code": 1,
    "year": "2021",
}, format="df")
```

### RBI / Trade Statistics

```python
# RBI uses sub_indicator_code internally; pass indicator_code and it maps automatically
meta = esankhyiki.get_metadata("RBI", indicator_code=1)

df = esankhyiki.get_data("RBI", {
    "indicator_code": 1,
    "year": "2023-24",
}, format="df")
```

---

## Error Handling

```python
from esankhyiki.exceptions import (
    InvalidDatasetError,
    InvalidFilterError,
    APIError,
    NoDataError,
)

try:
    data = esankhyiki.get_data("PLFS", {
        "bogus_param": 1,
        "indicator_code": 1,
        "frequency_code": 1,
    })
except InvalidFilterError as e:
    print(e)  # Shows invalid params and valid alternatives
except InvalidDatasetError as e:
    print(e)  # Shows valid dataset names
except NoDataError as e:
    print(e)  # Valid request, but no matching rows
except APIError as e:
    print(e)  # Upstream API / network / server failure
```

**Error contract:**

| Exception | When raised |
|-----------|-------------|
| `InvalidDatasetError` | Dataset name is not one of the 19 known datasets |
| `InvalidFilterError` | A filter param is missing, invalid, or not accepted by the endpoint |
| `NoDataError` | Request was valid but returned zero rows |
| `APIError` | Network failure, timeout, or upstream 5xx error |

---

## Live API Notes

- This package wraps live MoSPI endpoints. Some datasets may temporarily return `No Data Found` or upstream 5xx errors even when the code and filters are valid.
- Those cases surface explicitly as `NoDataError` or `APIError` rather than silently returning empty results.
- The recommended workflow is always: `list_datasets()` -> `get_indicators()` -> `get_metadata()` -> `get_data()`.
- The client retries on 429, 500, 502, 503, and 504 status codes (up to 3 times with backoff).

---

## Testing

```bash
# Non-network contract tests only
pytest -q -m "not network"

# All tests including live endpoint calls
pytest -q
```

To verify release artifacts locally:

```bash
python -m build
```

---

## Related

- [e-Sankhyiki MCP Server](https://github.com/nso-india/esankhyiki-mcp) - MCP server for accessing MoSPI data through AI assistants (Claude, ChatGPT, Cursor, etc.)
- [MoSPI Open APIs](https://api.mospi.gov.in) - Official API documentation and e-Sankhyiki portal

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

Made in partnership with **[Bharat Digital](https://bharatdigital.io)** in pursuit of modernising and humanising how governments use technology in service of the public.
