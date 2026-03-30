"""Tests for nsoindia.get_data() -requires network access."""

import pandas as pd
import pytest
import nsoindia
from nsoindia.exceptions import InvalidDatasetError, InvalidFilterError

pytestmark = pytest.mark.network


def test_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        nsoindia.get_data("FAKE", {})


def test_plfs_data():
    result = nsoindia.get_data("PLFS", {
        "indicator_code": 1,
        "frequency_code": 1,
        "year_type_code": 1,
        "year": "2023-24",
        "state_code": 99,
        "gender_code": 3,
        "age_code": 1,
        "sector_code": 3,
    })
    assert isinstance(result, (dict, list))


def test_nas_data():
    result = nsoindia.get_data("NAS", {
        "indicator_code": 1,
        "base_year": "2022-23",
        "series": "Current",
        "frequency_code": 1,
    })
    assert isinstance(result, (dict, list))


def test_cpi_auto_routes_group():
    result = nsoindia.get_data("CPI", {
        "base_year": "2024",
        "year": "2026",
        "series": "Current",
    })
    assert isinstance(result, (dict, list))


def test_invalid_filter_raises():
    with pytest.raises(InvalidFilterError):
        nsoindia.get_data("PLFS", {"bogus_param": "123", "indicator_code": 1, "frequency_code": 1, "year_type_code": 1})


def test_asi_data_with_required_filters():
    result = nsoindia.get_data("ASI", {
        "classification_year": "2008",
        "indicator_code": 1,
        "year": "2022-23",
        "sector_code": "Combined",
        "nic_type": "All",
    })
    assert isinstance(result, (dict, list))


def test_ec_df_format_returns_dataframe():
    result = nsoindia.get_data("EC", {
        "indicator_code": 1,
        "state": "27",
        "mode": "detail",
        "pageNum": "1",
    }, format="df")
    assert isinstance(result, pd.DataFrame)
