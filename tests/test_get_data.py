"""Tests for esankhyiki.get_data().

These tests require network access to the MoSPI APIs.
"""

import pandas as pd
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

NSS_DATASETS = [
    (
        "NSS75",
        {
            "survey_code": 1,
            "indicator_code": 1,
            "limit": 20,
        },
    ),
    (
        "NSS75E",
        {
            "survey_code": 2,
            "indicator_code": 43,
            "limit": 20,
        },
    ),
    (
        "NSS76",
        {
            "survey_code": 2,
            "indicator_code": 2,
            "limit": 20,
        },
    ),
    (
        "NSS76C",
        {
            "survey_code": 1,
            "indicator_code": 13,
            "limit": 20,
        },
    ),
    (
        "NSS80",
        {
            "survey_code": 1,
            "indicator_code": 12,
            "limit": 20,
        },
    ),
    (
        "NSS80C",
        {
            "survey_code": 2,
            "indicator_code": 29,
            "limit": 20,
        },
    ),
]


# ============================================================================
# Helpers
# ============================================================================

def assert_dict_or_list(dataset: str, filters: dict):
    """Assert that get_data returns a dictionary or list."""

    result = esankhyiki.get_data(dataset, filters)

    assert isinstance(result, (dict, list))


def assert_dataframe(dataset: str, filters: dict):
    """Assert that get_data returns a pandas DataFrame."""

    result = esankhyiki.get_data(
        dataset,
        filters,
        format="df",
    )

    assert isinstance(result, pd.DataFrame)


def assert_network_dataset(dataset: str, filters: dict, fmt="dict"):
    """
    Helper for datasets whose APIs may occasionally return
    APIError or NoDataError.
    """

    try:
        result = esankhyiki.get_data(
            dataset,
            filters,
            format=fmt,
        )

    except (APIError, NoDataError) as exc:
        assert str(exc)

    else:
        if fmt == "df":
            assert isinstance(result, pd.DataFrame)
        else:
            assert isinstance(result, (dict, list))


# ============================================================================
# Validation
# ============================================================================

def test_invalid_dataset_raises():
    """Unknown dataset should raise InvalidDatasetError."""

    with pytest.raises(InvalidDatasetError):
        esankhyiki.get_data("FAKE", {})


def test_invalid_filter_raises():
    """Invalid filter should raise InvalidFilterError."""

    with pytest.raises(InvalidFilterError):
        esankhyiki.get_data(
            "PLFS",
            {
                "bogus_param": "123",
                "indicator_code": 1,
                "frequency_code": 1,
                "year_type_code": 1,
            },
        )


# ============================================================================
# PLFS
# ============================================================================

def test_plfs_data():
    """PLFS data retrieval."""

    assert_dict_or_list(
        "PLFS",
        {
            "indicator_code": 1,
            "frequency_code": 1,
            "year_type_code": 1,
            "year": "2023-24",
            "state_code": 99,
            "gender_code": 3,
            "age_code": 1,
            "sector_code": 3,
        },
    )


# ============================================================================
# NAS
# ============================================================================

def test_nas_data():
    """NAS data retrieval."""

    assert_dict_or_list(
        "NAS",
        {
            "indicator_code": 1,
            "base_year": "2022-23",
            "series": "Current",
            "frequency_code": 1,
        },
    )


# ============================================================================
# ISP
# ============================================================================

def test_isp_data():
    """ISP data retrieval."""

    assert_dict_or_list(
        "ISP",
        {
            "frequency_code": 1,
            "limit": 1,
        },
    )


# ============================================================================
# NSS73
# ============================================================================

def test_nss73_data():
    """NSS73 data retrieval."""

    assert_dict_or_list(
        "NSS73",
        {
            "indicator_code": 6,
            "limit": 20,
        },
    )


# ============================================================================
# NSS Datasets
# ============================================================================

@pytest.mark.parametrize(
    ("dataset", "filters"),
    NSS_DATASETS,
)
def test_nss_data(dataset, filters):
    """Data retrieval for all supported NSS datasets."""

    assert_dict_or_list(dataset, filters)


# ============================================================================
# CPI
# ============================================================================

def test_cpi_auto_routes_group():
    """Verify CPI auto-routing."""

    assert_dict_or_list(
        "CPI",
        {
            "base_year": "2024",
            "year": "2026",
            "series": "Current",
        },
    )


# ============================================================================
# ASI
# ============================================================================

def test_asi_data():
    """ASI data retrieval."""

    assert_dict_or_list(
        "ASI",
        {
            "classification_year": "2008",
            "indicator_code": 1,
            "year": "2022-23",
            "sector_code": "Combined",
            "nic_type": "All",
        },
    )


# ============================================================================
# EC
# ============================================================================

def test_ec_dataframe():
    """EC dataframe output."""

    assert_dataframe(
        "EC",
        {
            "indicator_code": 1,
            "state": "27",
            "mode": "detail",
            "pageNum": "1",
        },
    )


# ============================================================================
# MNRE
# ============================================================================

def test_mnre_data():
    """MNRE dictionary response."""

    assert_network_dataset(
        "MNRE",
        {
            "type_of_renewable_energy_code": 1,
            "state_code": 36,
            "year": "2023",
        },
    )


def test_mnre_dataframe():
    """MNRE dataframe response."""

    assert_network_dataset(
        "MNRE",
        {
            "type_of_renewable_energy_code": 2,
            "state_code": 36,
        },
        fmt="df",
    )