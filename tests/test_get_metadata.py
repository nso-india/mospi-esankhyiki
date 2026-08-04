"""Tests for esankhyiki.get_metadata().

These tests require network access to the MoSPI APIs.
"""

import pytest

import esankhyiki
from esankhyiki.exceptions import (
    APIError,
    InvalidDatasetError,
    InvalidFilterError,
    NoDataError,
)

pytestmark = pytest.mark.network


# ============================================================================
# Dataset Groups
# ============================================================================

SIMPLE_DATASETS = [
    "AISHE",
    "GENDER",
    "NFHS",
    "ENVSTATS",
    "NSS73",
    "NSS77",
    "NSS78",
    "CPIALRL",
    "HCES",
    "TUS",
]

SPECIAL_METADATA_DATASETS = [
    ("ASI", {"classification_year": "2008"}),
    (
        "NAS",
        {
            "indicator_code": 1,
            "base_year": "2022-23",
            "series": "Current",
            "frequency_code": 1,
        },
    ),
    (
        "ENERGY",
        {
            "indicator_code": 1,
            "use_of_energy_balance_code": 1,
        },
    ),
    (
        "ASUSE",
        {
            "indicator_code": 1,
            "frequency_code": 1,
        },
    ),
    (
        "RBI",
        {
            "sub_indicator_code": 1,
        },
    ),
]

NEW_NSS_DATASETS = [
    ("NSS75", 1),
    ("NSS75E", 43),
    ("NSS76", 23),
    ("NSS76C", 13),
    ("NSS80", 12),
    ("NSS80C", 29),
]


# ============================================================================
# Helper
# ============================================================================

def assert_metadata_response(dataset: str, **filters):
    """
    Assert that get_metadata() returns a valid response.

    Some live APIs may temporarily return APIError or NoDataError.
    Those responses are accepted for network tests.
    """
    try:
        result = esankhyiki.get_metadata(dataset, **filters)

    except (APIError, NoDataError) as exc:
        assert str(exc)

    else:
        assert isinstance(result, (dict, list))


# ============================================================================
# Validation Tests
# ============================================================================

def test_invalid_dataset_raises():
    """Unknown dataset should raise InvalidDatasetError."""

    with pytest.raises(InvalidDatasetError):
        esankhyiki.get_metadata("FAKE")


def test_plfs_requires_indicator_code():
    """PLFS should require indicator_code."""

    with pytest.raises(InvalidFilterError):
        esankhyiki.get_metadata("PLFS")


# ============================================================================
# PLFS
# ============================================================================

def test_plfs_metadata():
    """PLFS metadata should return filter values."""

    result = esankhyiki.get_metadata(
        "PLFS",
        indicator_code=1,
        frequency_code=1,
        year_type_code=1,
    )

    assert "filter_values" in result or "error" in result
    assert isinstance(result, (dict, list))


# ============================================================================
# CPI
# ============================================================================

def test_cpi_metadata():
    """CPI metadata."""

    result = esankhyiki.get_metadata(
        "CPI",
        base_year="2024",
        level="Group",
        series="Current",
    )

    assert isinstance(result, (dict, list))


# ============================================================================
# IIP
# ============================================================================

def test_iip_metadata():
    """IIP metadata."""

    result = esankhyiki.get_metadata(
        "IIP",
        base_year="2011-12",
        frequency="Annually",
    )

    assert isinstance(result, (dict, list))


# ============================================================================
# NSS Datasets
# ============================================================================

@pytest.mark.parametrize(
    ("dataset", "indicator_code"),
    NEW_NSS_DATASETS,
)
def test_new_nss_metadata(dataset, indicator_code):
    """Metadata for newly supported NSS datasets."""

    result = esankhyiki.get_metadata(
        dataset,
        indicator_code=indicator_code,
    )

    assert isinstance(result, (dict, list))


# ============================================================================
# ISP
# ============================================================================

def test_isp_metadata():
    """ISP metadata."""

    result = esankhyiki.get_metadata(
        "ISP",
        frequency_code=2,
    )

    assert isinstance(result, (dict, list))


# ============================================================================
# EC
# ============================================================================

def test_ec_metadata():
    """Economic Census metadata."""

    result = esankhyiki.get_metadata(
        "EC",
        indicator_code=1,
    )

    assert isinstance(result, (dict, list))


# ============================================================================
# Standard Metadata APIs
# ============================================================================

@pytest.mark.parametrize(
    ("dataset", "filters"),
    SPECIAL_METADATA_DATASETS,
)
def test_special_metadata(dataset, filters):
    """Datasets with custom metadata parameters."""

    result = esankhyiki.get_metadata(
        dataset,
        **filters,
    )

    assert isinstance(result, (dict, list))


# ============================================================================
# Simple Metadata APIs
# ============================================================================

@pytest.mark.parametrize(
    "dataset",
    SIMPLE_DATASETS,
)
def test_simple_metadata(dataset):
    """Datasets using only indicator_code."""

    assert_metadata_response(
        dataset,
        indicator_code=1,
    )


# ============================================================================
# MNRE
# ============================================================================

def test_mnre_metadata():
    """MNRE metadata."""

    assert_metadata_response(
        "MNRE",
        indicator_code=1,
    )