"""
Output format conversions for mospi API responses.

Supported formats: "dict" (default), "df" / "dataframe", "csv"
"""

import io
import csv as csv_mod
from typing import Any, Union

from .exceptions import APIError, NoDataError


def _extract_records(result: dict) -> list:
    """Extract the list of records from an API response dict.

    Handles all response shapes:
      - result["data"] = list               (most datasets)
      - result["data"]["indicator"] = list   (NAS, ENERGY, CPIALRL)
      - result["data"]["data"] = list        (some nested responses)
      - result["data"] = dict with lists     (CPI indicators -flatten each sub-list)
      - result["indicators_by_frequency"]    (PLFS, ASUSE -flatten all groups)
      - result["indicator"] = list           (NSS78)
      - result["filter_values"]             (metadata responses)
      - result["datasets"]                  (list_datasets)

    The "data" key always takes priority; other keys are only used when "data" is absent.
    """
    data = result.get("data")

    if data is not None:
        # Most common: data is a plain list of records
        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            # Nested: data.indicator or data.data
            if "indicator" in data and isinstance(data["indicator"], list):
                return data["indicator"]
            if "data" in data and isinstance(data["data"], list):
                return data["data"]
            # Dict of lists (e.g. CPI get_indicators: {base_year:[..], level:[..], series:[..]})
            lists_of_dicts = []
            for key, values in data.items():
                if isinstance(values, list) and values:
                    normalized_values = []
                    for v in values:
                        if isinstance(v, dict):
                            normalized_values.append(v)
                        else:
                            normalized_values.append({key: v})
                    if normalized_values:
                        lists_of_dicts.append(normalized_values)
            
            if lists_of_dicts:
                # Guard against cartesian explosion on large filter responses
                # (e.g. WPI with 7 lists of 15-300 items each).
                # Only compute product for small lists (< 10K combinations).
                total = 1
                for lst in lists_of_dicts:
                    total *= max(len(lst), 1)
                    if total > 10000:
                        break
                if total <= 10000:
                    import itertools
                    rows = []
                    for combo in itertools.product(*lists_of_dicts):
                        row = {}
                        for d_item in combo:
                            row.update(d_item)
                        rows.append(row)
                    return rows
                else:
                    # Too large for product - flatten each list separately
                    rows = []
                    for lst in lists_of_dicts:
                        rows.extend(lst)
                    return rows

        return []

    # "data" key absent — fall through to dataset-specific shapes

    # PLFS/ASUSE frequency-grouped or NSS79 survey-grouped indicators
    if "indicators_by_survey" in result:
        rows = []
        for group_name, items in result["indicators_by_survey"].items():
            if isinstance(items, list):
                for item in items:
                    row = dict(item) if isinstance(item, dict) else {"value": item}
                    row["survey_group"] = group_name
                    rows.append(row)
        return rows

    if "indicators_by_frequency" in result:
        rows = []
        for group_name, items in result["indicators_by_frequency"].items():
            if isinstance(items, list):
                for item in items:
                    row = dict(item) if isinstance(item, dict) else {"value": item}
                    row["frequency_group"] = group_name
                    rows.append(row)
        return rows

    # NSS78-style
    if "indicator" in result and isinstance(result["indicator"], list):
        return result["indicator"]

    # filter_values (metadata responses)
    fv = result.get("filter_values")
    if isinstance(fv, dict):
        return _extract_records(fv)

    # list_datasets() shape
    datasets = result.get("datasets")
    if isinstance(datasets, list):
        return [{"dataset": d} for d in datasets]
    if isinstance(datasets, dict):
        rows = []
        for dataset, info in datasets.items():
            row = {"dataset": dataset}
            if isinstance(info, dict):
                row.update(info)
            else:
                row["value"] = info
            rows.append(row)
        if rows:
            return rows

    return []


def to_dataframe(result: dict) -> Any:
    """Convert API response to a pandas DataFrame.

    Raises ImportError if pandas is not installed.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for DataFrame output. "
            "Install it with: pip install pandas"
        )

    records = _extract_records(result)
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def to_csv(result: dict) -> str:
    """Convert API response to a CSV string."""
    records = _extract_records(result)
    if not records:
        return ""

    output = io.StringIO()
    # Collect all keys across all records for the header
    fieldnames = list(dict.fromkeys(k for row in records for k in row.keys()))
    writer = csv_mod.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue()


def _strip_viz(obj):
    """Recursively remove 'viz' and 'viz_status' keys from dicts in the response."""
    if isinstance(obj, dict):
        obj.pop("viz", None)
        obj.pop("viz_status", None)
        for v in obj.values():
            _strip_viz(v)
    elif isinstance(obj, list):
        for item in obj:
            _strip_viz(item)


def format_response(result: dict, fmt: str) -> Union[dict, Any, str]:
    """Apply the requested output format to an API response.

    Args:
        result: Raw API response dict.
        fmt: One of "dict", "df", "dataframe", "csv".

    Returns:
        dict, pandas.DataFrame, or CSV string.
    """
    _strip_viz(result)
    fmt = fmt.lower().strip()

    if isinstance(result, dict) and "error" in result:
        raise APIError(
            result["error"],
            dataset=result.get("dataset"),
            filters=result.get("filters"),
            troubleshooting=result.get("troubleshooting"),
            suggestion=result.get("suggestion"),
            response=result,
        )

    # Check for "No Data Found" without calling _extract_records (which can
    # be expensive for large dict-of-lists responses like WPI filters).
    if isinstance(result, dict):
        msg = result.get("msg")
        ts = result.get("troubleshooting")
        if (msg == "No Data Found" and not result.get("data")) or (ts and not result.get("data")):
            message = msg if msg and msg != "Data fetched successfully" else (
                ts or "No data found for the requested query."
            )
            raise NoDataError(
                message,
                dataset=result.get("dataset"),
                filters=result.get("filters"),
                troubleshooting=ts,
                suggestion=result.get("suggestion"),
                response=result,
            )

    if fmt == "dict":
        if isinstance(result, dict) and "data" in result:
            return result["data"]
        return result
    elif fmt in ("df", "dataframe"):
        return to_dataframe(result)
    elif fmt == "csv":
        return to_csv(result)
    else:
        raise ValueError(f"Unknown format: '{fmt}'. Use 'dict', 'df', or 'csv'.")
