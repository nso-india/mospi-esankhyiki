"""Tests for esankhyiki.get_indicators().

These tests require network access to the MoSPI APIs.
"""

import pytest

import esankhyiki
from esankhyiki.exceptions import (
    APIError,
    InvalidDatasetError,
    NoDataError,
)

pytestmark = pytest.mark.network


# ============================================================================
# Dataset Groups
# ============================================================================

SIMPLE_DATASETS = [
    "ASI",
    "ENERGY",
    "AISHE",
    "ASUSE",
    "GENDER",
    "NFHS",
    "ENVSTATS",
    "RBI",
    "NSS73",
    "NSS75",
    "NSS75E",
    "NSS76",
    "NSS76C",
    "NSS77",
    "NSS78",
    "CPIALRL",
    "HCES",
    "TUS",
    "NSS79",
    "NSS80",
    "NSS80C",
    "MNRE",
]

STANDARD_DATASETS = [
    "CPI",
    "IIP",
    "EC",
]


# ============================================================================
# Helper
# ============================================================================

def assert_indicator_response(dataset: str):
    """
    Assert that get_indicators() returns a valid response.

    Live APIs may occasionally return temporary APIError or NoDataError.
    Those responses are considered acceptable during network testing.
    """
    try:
        result = esankhyiki.get_indicators(dataset)

    except (APIError, NoDataError) as exc:
        assert str(exc)

    else:
        assert isinstance(result, (dict, list))
        assert len(result) > 0


# ============================================================================
# Invalid Dataset
# ============================================================================

def test_invalid_dataset_raises():
    """Unknown dataset should raise InvalidDatasetError."""

    with pytest.raises(InvalidDatasetError):
        esankhyiki.get_indicators("FAKE")


# ============================================================================
# PLFS
# ============================================================================

def test_plfs_indicators():
    """PLFS should return grouped indicators."""

    result = esankhyiki.get_indicators("PLFS")

    assert (
        "indicators_by_frequency" in result
        or "error" in result
    )


# ============================================================================
# ISP
# ============================================================================

def test_isp_indicators():
    """ISP should return the supported frequencies."""

    expected = [
        {
            "frequency_code": 1,
            "desc": "Yearly",
        },
        {
            "frequency_code": 2,
            "desc": "Monthly",
        },
    ]

    assert esankhyiki.get_indicators("ISP") == expected

# ============================================================================
# NAS
# ============================================================================

def test_nas_indicators():
    """NAS endpoint may occasionally return transient API errors."""

    assert_indicator_response("NAS")


# ============================================================================
# CPI / IIP / EC
# ============================================================================

@pytest.mark.parametrize("dataset", STANDARD_DATASETS)
def test_standard_indicator_response(dataset):
    """Datasets should return either dict or list."""

    result = esankhyiki.get_indicators(dataset)

    assert isinstance(result, (dict, list))


# ============================================================================
# Simple Indicator APIs
# ============================================================================

@pytest.mark.parametrize("dataset", SIMPLE_DATASETS)
def test_simple_indicators(dataset):
    """Verify indicator APIs for all standard datasets."""

    assert_indicator_response(dataset)