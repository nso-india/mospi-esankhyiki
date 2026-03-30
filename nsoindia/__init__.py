"""
nsoindia -Python client for India's Ministry of Statistics (MoSPI) data portal.

4-step workflow:
    1. nsoindia.list_datasets()           -discover available datasets
    2. nsoindia.get_indicators(dataset)   -list indicators for a dataset
    3. nsoindia.get_metadata(dataset, ..) -get valid filter values
    4. nsoindia.get_data(dataset, filters)— fetch statistical data
"""

from typing import Dict, Any

from .client import MoSPI
from .datasets import (
    VALID_DATASETS,
    DATASET_API_MAP,
    get_swagger_param_definitions,
    get_required_metadata_params,
    validate_filters,
    transform_filters,
    enrich_indicators,
    resolve_dataset_name,
)
from .exceptions import MospiError, InvalidDatasetError, InvalidFilterError, APIError, NoDataError
from .formatters import format_response

__version__ = "0.1.0"
__all__ = ["list_datasets", "get_indicators", "get_metadata", "get_data"]

# Module-level client instance
_client = MoSPI()


def _safe_int(value, param_name: str):
    """Validate and coerce a value to int."""
    if value is None:
        return None, None
    try:
        return int(value), None
    except (ValueError, TypeError):
        return None, {"error": f"{param_name} must be an integer, got: {value!r}"}


def _coerce_int_or_raise(value, param_name: str):
    """Validate and coerce a value to int, raising InvalidFilterError on failure."""
    value, err = _safe_int(value, param_name)
    if err:
        raise InvalidFilterError(err["error"], invalid_params=[param_name])
    return value



def _check_empty_metadata(result, dataset, **params):
    """Raise NoDataError if upstream returned empty filter values."""
    if "error" in result:
        return result
        
    data = result.get("filter_values", result.get("data", {}))
    if isinstance(data, dict):
        inner = data.get("data", data)
        if isinstance(inner, dict):
            values = [v for v in inner.values() if isinstance(v, list)]
            is_empty = (not inner) or (values and all(len(v) == 0 for v in values))
        else:
            is_empty = False
    else:
        is_empty = False

    if is_empty:
        param_str = ", ".join(f"{k}={v}" for k, v in params.items() if v is not None)
        raise NoDataError(
            f"No filter values returned for {dataset} with {param_str}",
            dataset=dataset,
            filters=params,
        )
    return result


# =========================================================================
# Step 1: list_datasets
# =========================================================================

def list_datasets(format: str = "dict"):
    """
    Returns an overview of all 19 MoSPI statistical datasets.

    This is the starting point -call this first to identify the right dataset.

    Args:
        format: Output format -"dict" (default), "df"/"dataframe", or "csv".

    Returns:
        dict, pandas DataFrame, or CSV string.
    """
    result = {"datasets": VALID_DATASETS}
    return format_response(result, format)


# =========================================================================
# Step 2: get_indicators
# =========================================================================

def get_indicators(
    dataset: str,
    format: str = "dict",
):
    """
    Returns available indicators for a given dataset.

    Step 2 of: list_datasets -> get_indicators -> get_metadata -> get_data

    Args:
        dataset: Dataset name (PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, AISHE,
                 ASUSE, GENDER, NFHS, ENVSTATS, RBI, NSS77, NSS78, CPIALRL,
                 HCES, TUS, EC).
        format: Output format -"dict" (default), "df"/"dataframe", or "csv".

    Returns:
        dict, pandas DataFrame, or CSV string.
    """
    dataset = resolve_dataset_name(dataset)

    indicator_methods = {
        "PLFS": _client.get_plfs_indicators,
        "NAS": _client.get_nas_indicators,
        "ENERGY": _client.get_energy_indicators,
        "AISHE": _client.get_aishe_indicators,
        "ASUSE": _client.get_asuse_indicators,
        "GENDER": _client.get_gender_indicators,
        "NFHS": _client.get_nfhs_indicators,
        "ENVSTATS": _client.get_envstats_indicators,
        "RBI": _client.get_rbi_indicators,
        "NSS77": _client.get_nss77_indicators,
        "NSS78": _client.get_nss78_indicators,
        "CPIALRL": _client.get_cpialrl_indicators,
        "HCES": _client.get_hces_indicators,
        "TUS": _client.get_tus_indicators,
        "EC": _client.get_ec_indicators,
        "CPI": _client.get_cpi_base_years,
        "IIP": lambda: {"dataset": "IIP"},
        "WPI": lambda: {"dataset": "WPI"},
        "ASI": _client.get_asi_indicators,
    }

    result = indicator_methods[dataset]()
    result = enrich_indicators(result, dataset)
    return format_response(result, format)


# =========================================================================
# Step 3: get_metadata
# =========================================================================

def get_metadata(
    dataset: str,
    indicator_code=None,
    base_year=None,
    level=None,
    frequency=None,
    classification_year=None,
    frequency_code=None,
    series=None,
    use_of_energy_balance_code=None,
    sub_indicator_code=None,
    year_type_code=None,
    format: str = "dict",
):
    """
    Returns valid filter values (states, years, quarters, etc.) for a dataset and indicator.

    Step 3 of: list_datasets -> get_indicators -> get_metadata -> get_data

    Args:
        dataset: Dataset name.
        indicator_code: Required for most datasets. Not needed for CPI, IIP, ASI, WPI.
        base_year: Required for CPI, IIP, NAS.
        level: Required for CPI ("Group"/"Item").
        frequency: Required for IIP ("Annually"/"Monthly").
        classification_year: Required for ASI.
        frequency_code: Required for PLFS and ASUSE.
        series: For CPI and NAS ("Current"/"Back").
        use_of_energy_balance_code: For ENERGY (1=Supply, 2=Consumption).
        sub_indicator_code: For RBI (alternative to indicator_code).
        format: Output format -"dict" (default), "df"/"dataframe", or "csv".

    Returns:
        dict, pandas DataFrame, or CSV string.
    """
    dataset = resolve_dataset_name(dataset)

    indicator_code = _coerce_int_or_raise(indicator_code, "indicator_code")
    frequency_code = _coerce_int_or_raise(frequency_code, "frequency_code")
    use_of_energy_balance_code = _coerce_int_or_raise(
        use_of_energy_balance_code, "use_of_energy_balance_code"
    )
    sub_indicator_code = _coerce_int_or_raise(sub_indicator_code, "sub_indicator_code")

    # Validate required params derived from swagger spec
    _param_values = {
        "indicator_code": indicator_code,
        "frequency_code": frequency_code,
        "base_year": base_year,
        "level": level,
        "frequency": frequency,
        "classification_year": classification_year,
        "series": series,
        "use_of_energy_balance_code": use_of_energy_balance_code,
        "sub_indicator_code": sub_indicator_code,
        "year_type_code": year_type_code,
    }
    _required = get_required_metadata_params(dataset)
    _missing = [p for p in _required if _param_values.get(p) is None]
    if _missing:
        raise InvalidFilterError(
            f"Missing required params for get_metadata(dataset='{dataset}'): {_missing}",
            invalid_params=_missing,
        )

    try:
        if dataset == "CPI":
            swagger_key = "CPI_ITEM" if (level or "Group") == "Item" else "CPI_GROUP"
            result = _client.get_cpi_filters(
                base_year=base_year or "2024",
                level=level or "Group",
                series_code=series or "Current",
            )
            result["api_params"] = get_swagger_param_definitions(swagger_key)
            result = _check_empty_metadata(result, dataset, base_year=base_year, level=level, series=series)

        elif dataset == "IIP":
            swagger_key = "IIP_MONTHLY" if (frequency or "Annually") == "Monthly" else "IIP_ANNUAL"
            result = _client.get_iip_filters(base_year=base_year or "2011-12", frequency=frequency or "Annually")
            result["api_params"] = get_swagger_param_definitions(swagger_key)
            result = _check_empty_metadata(result, dataset, base_year=base_year, frequency=frequency)

        elif dataset == "ASI":
            result = _client.get_asi_filters(classification_year=classification_year or "2008")
            result["api_params"] = get_swagger_param_definitions("ASI")
            result = _check_empty_metadata(result, dataset, classification_year=classification_year)

        elif dataset == "WPI":
            result = _client.get_wpi_filters()
            result["api_params"] = get_swagger_param_definitions("WPI")

        elif dataset == "PLFS":
            filters = _client.get_plfs_filters(indicator_code=indicator_code, frequency_code=frequency_code or 1)
            result = {
                "dataset": "PLFS",
                "filter_values": filters,
                "api_params": get_swagger_param_definitions("PLFS"),
            }
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code, frequency_code=frequency_code)

        elif dataset == "NAS":
            result = _client.get_nas_filters(
                series=series or "Current", frequency_code=frequency_code or 1,
                indicator_code=indicator_code, base_year=base_year or "2022-23",
            )
            result["api_params"] = get_swagger_param_definitions("NAS")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code, base_year=base_year)

        elif dataset == "ENERGY":
            result = _client.get_energy_filters(
                indicator_code=indicator_code or 1,
                use_of_energy_balance_code=use_of_energy_balance_code or 1,
            )
            result["api_params"] = get_swagger_param_definitions("ENERGY")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "AISHE":
            result = _client.get_aishe_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("AISHE")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "ASUSE":
            result = _client.get_asuse_filters(indicator_code=indicator_code, frequency_code=frequency_code or 1)
            result["api_params"] = get_swagger_param_definitions("ASUSE")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "GENDER":
            result = _client.get_gender_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("GENDER")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "NFHS":
            result = _client.get_nfhs_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("NFHS")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "ENVSTATS":
            result = _client.get_envstats_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("ENVSTATS")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "RBI":
            rbi_indicator = sub_indicator_code if sub_indicator_code is not None else indicator_code
            result = _client.get_rbi_filters(sub_indicator_code=rbi_indicator)
            result["api_params"] = get_swagger_param_definitions("RBI")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "NSS77":
            result = _client.get_nss77_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("NSS77")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "NSS78":
            result = _client.get_nss78_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("NSS78")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "CPIALRL":
            result = _client.get_cpialrl_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("CPIALRL")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "HCES":
            result = _client.get_hces_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("HCES")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "TUS":
            result = _client.get_tus_filters(indicator_code=indicator_code)
            result["api_params"] = get_swagger_param_definitions("TUS")
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        elif dataset == "EC":
            result = _client.get_ec_filters(indicator_code=indicator_code)
            result = _check_empty_metadata(result, dataset, indicator_code=indicator_code)

        else:
            raise InvalidDatasetError(dataset, VALID_DATASETS)

        return format_response(result, format)

    except MospiError:
        raise
    except Exception as e:
        raise APIError(str(e), dataset=dataset)


# =========================================================================
# Step 4: get_data
# =========================================================================

def get_data(dataset: str, filters: Dict[str, Any], format: str = "dict"):
    """
    Fetches statistical data from a MoSPI dataset.

    This is the final step. Use filter values from get_metadata().
    All filter parameters including limit and page go inside the filters dict.

    Step 4 of: list_datasets -> get_indicators -> get_metadata -> get_data

    Args:
        dataset: Dataset name (PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, AISHE,
                 ASUSE, GENDER, NFHS, ENVSTATS, RBI, NSS77, NSS78, CPIALRL,
                 HCES, TUS, EC).
        filters: Key-value pairs from get_metadata filter_values.
        format: Output format -"dict" (default), "df"/"dataframe", or "csv".

    Returns:
        dict, pandas DataFrame, or CSV string.
    """
    dataset = resolve_dataset_name(dataset)

    # EC uses a completely different API (POST to esankhyiki.nsoindia.gov.in)
    if dataset == "EC":
        transformed_filters = transform_filters(filters)
        ic = _coerce_int_or_raise(transformed_filters.get("indicator_code", 1), "indicator_code")
        result = _client.get_ec_data(indicator_code=ic, filters=transformed_filters)
        return format_response(result, format)

    # Auto-route CPI and IIP based on filters
    if dataset == "CPI":
        dataset = "CPI_ITEM" if "item_code" in filters else "CPI_GROUP"

    if dataset == "IIP":
        dataset = "IIP_MONTHLY" if "month_code" in filters else "IIP_ANNUAL"

    # IIP Annual: metadata returns 'year' but endpoint expects 'financial_year'
    if dataset == "IIP_ANNUAL":
        if "year" in filters and "financial_year" not in filters:
            filters = dict(filters)
            filters["financial_year"] = filters.pop("year")

    # IIP: auto-inject 'type' default if not provided
    if dataset in ("IIP_ANNUAL", "IIP_MONTHLY") and "type" not in filters:
        filters = dict(filters)
        filters["type"] = "All"

    # NSS78: map indicator_code to Indicator (API uses capital-I naming)
    if dataset == "NSS78" and "indicator_code" in filters and "Indicator" not in filters:
        filters = dict(filters)
        filters["Indicator"] = filters.pop("indicator_code")

    api_dataset = DATASET_API_MAP.get(dataset)
    if not api_dataset:
        raise InvalidDatasetError(dataset, VALID_DATASETS)

    transformed_filters = transform_filters(filters)

    # Auto-inject Format=JSON if not set (required by most endpoints)
    if "Format" not in transformed_filters:
        transformed_filters["Format"] = "JSON"

    # RBI: accept indicator_code but map to sub_indicator_code
    if dataset == "RBI" and "indicator_code" in transformed_filters:
        transformed_filters["sub_indicator_code"] = transformed_filters.pop("indicator_code")

    # Validate against swagger spec
    validation = validate_filters(dataset, transformed_filters)
    if not validation["valid"]:
        raise InvalidFilterError(
            validation.get("hint", "Invalid parameters"),
            invalid_params=validation.get("invalid_params"),
            valid_params=validation.get("valid_params"),
        )

    result = _client.get_data(api_dataset, transformed_filters)
    return format_response(result, format)
