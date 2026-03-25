"""
Dataset registry, swagger validation, and indicator enrichment utilities.
"""

import difflib
import os
import yaml
from typing import Dict, Any

SWAGGER_DIR = os.path.join(os.path.dirname(__file__), "swagger")

VALID_DATASETS = [
    "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY",
    "AISHE", "ASUSE", "GENDER", "NFHS", "ENVSTATS", "RBI",
    "NSS77", "NSS78", "CPIALRL", "HCES", "TUS", "EC",
]

DATASET_SWAGGER = {
    "PLFS": ("swagger_user_plfs.yaml", "/api/plfs/getData"),
    "CPI": ("swagger_user_cpi.yaml", "/api/cpi/getCPIIndex"),
    "CPI_GROUP": ("swagger_user_cpi.yaml", "/api/cpi/getCPIIndex"),
    "CPI_ITEM": ("swagger_user_cpi.yaml", "/api/cpi/getItemIndex"),
    "IIP": ("swagger_user_iip.yaml", "/api/iip/getIIPAnnual"),
    "IIP_ANNUAL": ("swagger_user_iip.yaml", "/api/iip/getIIPAnnual"),
    "IIP_MONTHLY": ("swagger_user_iip.yaml", "/api/iip/getIIPMonthly"),
    "ASI": ("swagger_user_asi.yaml", "/api/asi/getASIData"),
    "NAS": ("swagger_user_nas.yaml", "/api/nas/getNASData"),
    "WPI": ("swagger_user_wpi.yaml", "/api/wpi/getWpiRecords"),
    "ENERGY": ("swagger_user_energy.yaml", "/api/energy/getEnergyRecords"),
    "AISHE": ("swagger_user_aishe.yaml", "/api/aishe/getAisheRecords"),
    "ASUSE": ("swagger_user_asuse.yaml", "/api/asuse/getAsuseRecords"),
    "GENDER": ("swagger_user_gender.yaml", "/api/gender/getGenderRecords"),
    "NFHS": ("swagger_user_nfhs.yaml", "/api/nfhs/getNfhsRecords"),
    "ENVSTATS": ("swagger_user_envstats.yaml", "/api/env/getEnvStatsRecords"),
    "RBI": ("swagger_user_rbi.yaml", "/api/rbi/getRbiRecords"),
    "NSS77": ("swagger_user_nss77.yaml", "/api/nss-77/getNss77Records"),
    "NSS78": ("swagger_user_nss78.yaml", "/api/nss-78/getNss78Records"),
    "CPIALRL": ("swagger_user_cpialrl.yaml", "/api/cpialrl/getCpialrlRecords"),
    "HCES": ("swagger_user_hces.yaml", "/api/hces/getHcesRecords"),
    "TUS": ("swagger_user_tus.yaml", "/api/tus/getTusRecords"),
    "EC": ("swagger_user_ec.yaml", "/EC/filterDistrict6"),
}

# Dataset name -> API key mapping for get_data routing
DATASET_API_MAP = {
    "CPI_GROUP": "CPI_Group",
    "CPI_ITEM": "CPI_Item",
    "IIP_ANNUAL": "IIP_Annual",
    "IIP_MONTHLY": "IIP_Monthly",
    "PLFS": "PLFS",
    "ASI": "ASI",
    "NAS": "NAS",
    "WPI": "WPI",
    "ENERGY": "Energy",
    "AISHE": "AISHE",
    "ASUSE": "ASUSE",
    "GENDER": "GENDER",
    "NFHS": "NFHS",
    "ENVSTATS": "ENVSTATS",
    "RBI": "RBI",
    "NSS77": "NSS77",
    "NSS78": "NSS78",
    "CPIALRL": "CPIALRL",
    "HCES": "HCES",
    "TUS": "TUS",
}


# =========================================================================
# Dataset name resolution with fuzzy matching
# =========================================================================

def resolve_dataset_name(name: str) -> str:
    """
    Resolve a dataset name string to its canonical key (e.g. "PLFS").

    Accepts the exact key (case-insensitive) or a fuzzy approximation.
    Raises InvalidDatasetError with suggestions when no good match is found.
    """
    from .exceptions import InvalidDatasetError

    stripped = name.strip()
    upper = stripped.upper()

    if upper in VALID_DATASETS:
        return upper

    lower_keys = {k.lower(): k for k in VALID_DATASETS}
    matches = difflib.get_close_matches(stripped.lower(), lower_keys.keys(), n=3, cutoff=0.3)
    suggestions = [lower_keys[m] for m in matches]
    raise InvalidDatasetError(stripped, VALID_DATASETS, suggestions=suggestions)



# =========================================================================
# Swagger validation
# =========================================================================

def get_swagger_param_definitions(dataset: str) -> list:
    """Load full param definitions from swagger spec for a dataset."""
    dataset_upper = dataset.upper()
    if dataset_upper not in DATASET_SWAGGER:
        return []
    yaml_file, endpoint_path = DATASET_SWAGGER[dataset_upper]
    swagger_path = os.path.join(SWAGGER_DIR, yaml_file)
    if not os.path.exists(swagger_path):
        return []
    with open(swagger_path, "r") as f:
        spec = yaml.safe_load(f)
    return spec.get("paths", {}).get(endpoint_path, {}).get("get", {}).get("parameters", [])


def get_swagger_params(dataset: str) -> list:
    """Get list of valid param names for a dataset from swagger."""
    return [p["name"] for p in get_swagger_param_definitions(dataset)]


# Params that get_metadata accepts - used to filter swagger required list
# down to only the navigational params (not data-filter-only params).
_METADATA_PARAMS = frozenset({
    "indicator_code", "base_year", "level", "frequency",
    "classification_year", "frequency_code", "series",
    "use_of_energy_balance_code", "sub_indicator_code",
})

# Swagger param names that map to get_metadata param names
_SWAGGER_PARAM_ALIASES = {"Indicator": "indicator_code"}


def get_required_metadata_params(dataset: str) -> list:
    """
    Return the required params for get_metadata derived from swagger.

    Filters swagger required params to only those that get_metadata accepts,
    normalising any API-specific aliases (e.g. NSS78 uses 'Indicator').
    Excludes auto-injected params like 'type', 'Format'.
    """
    param_defs = get_swagger_param_definitions(dataset)
    required = []
    for p in param_defs:
        if not p.get("required"):
            continue
        name = _SWAGGER_PARAM_ALIASES.get(p["name"], p["name"])
        if name in _METADATA_PARAMS:
            required.append(name)
    return required


def validate_filters(dataset: str, filters: Dict[str, Any]) -> Dict[str, Any]:
    """Validate filters against swagger spec. Returns {"valid": True} or error dict."""
    param_defs = get_swagger_param_definitions(dataset)
    if not param_defs:
        return {"valid": True}

    valid_params = [p["name"] for p in param_defs]

    invalid = [k for k in filters.keys() if k not in valid_params]
    if invalid:
        return {
            "valid": False,
            "invalid_params": invalid,
            "valid_params": valid_params,
            "hint": f"Invalid params: {invalid}. Valid params: {valid_params}.",
        }

    missing = [
        p["name"] for p in param_defs
        if p.get("required") and p["name"] != "Format" and p["name"] not in filters
    ]
    if missing:
        return {
            "valid": False,
            "missing_required": missing,
            "hint": f"Missing required params: {missing}.",
        }

    return {"valid": True}


def transform_filters(filters: Dict[str, Any]) -> Dict[str, str]:
    """Transform filters: skip None, convert floats to int, stringify all values."""
    result = {}
    for k, v in filters.items():
        if v is None:
            continue
        if isinstance(v, float) and v.is_integer():
            v = int(v)
        result[k] = str(v)
    return result


# =========================================================================
# Indicator enrichment
# =========================================================================


def _strip_viz(indicators: list) -> None:
    """In-place: remove the 'viz' field from each indicator dict."""
    for indicator in indicators:
        indicator.pop("viz", None)


def enrich_indicators(result: Dict[str, Any], dataset: str = None) -> Dict[str, Any]:
    """Strip internal viz field from indicator lists."""
    data = result.get("data")

    if isinstance(data, list):
        _strip_viz(data)
    elif isinstance(data, dict) and "indicator" in data:
        _strip_viz(data["indicator"])
    elif isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                _strip_viz(v)
    elif "indicators_by_frequency" in result:
        for items in result["indicators_by_frequency"].values():
            _strip_viz(items)
    elif "indicator" in result and isinstance(result["indicator"], list):
        _strip_viz(result["indicator"])

    return result
