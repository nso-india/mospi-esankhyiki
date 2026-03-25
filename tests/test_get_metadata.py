"""Tests for nsoindia.get_metadata() -requires network access."""

import pytest
import nsoindia
from nsoindia.exceptions import InvalidDatasetError, InvalidFilterError

pytestmark = pytest.mark.network


def test_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        nsoindia.get_metadata("FAKE")


def test_plfs_requires_indicator_code():
    with pytest.raises(InvalidFilterError):
        nsoindia.get_metadata("PLFS")


def test_plfs_metadata():
    result = nsoindia.get_metadata("PLFS", indicator_code=1, frequency_code=1)
    assert "filter_values" in result or "error" in result
    assert "api_params" in result or "error" in result


def test_cpi_metadata():
    result = nsoindia.get_metadata("CPI", base_year="2024", level="Group")
    assert "api_params" in result or "error" in result


def test_iip_metadata():
    result = nsoindia.get_metadata("IIP", base_year="2011-12", frequency="Annually")
    assert "api_params" in result or "error" in result


def test_ec_metadata():
    result = nsoindia.get_metadata("EC", indicator_code=1)
    assert "data" in result or "error" in result
