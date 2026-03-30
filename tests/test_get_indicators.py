"""Tests for nsoindia.get_indicators() -requires network access."""

import pytest
import nsoindia
from nsoindia.exceptions import APIError, InvalidDatasetError, NoDataError

pytestmark = pytest.mark.network


def test_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        nsoindia.get_indicators("FAKE")


def test_plfs_indicators():
    result = nsoindia.get_indicators("PLFS")
    assert "indicators_by_frequency" in result or "error" in result


def test_cpi_indicators():
    result = nsoindia.get_indicators("CPI")
    assert isinstance(result, (dict, list))


def test_iip_indicators():
    result = nsoindia.get_indicators("IIP")
    assert isinstance(result, (dict, list))


def test_wpi_indicators():
    result = nsoindia.get_indicators("WPI")
    assert isinstance(result, (dict, list))


def test_nas_indicators():
    try:
        result = nsoindia.get_indicators("NAS")
    except (NoDataError, APIError) as exc:
        assert str(exc)
    else:
        assert isinstance(result, (dict, list))


def test_ec_indicators():
    result = nsoindia.get_indicators("EC")
    assert isinstance(result, (dict, list))


@pytest.mark.parametrize("dataset", [
    "ASI", "ENERGY", "AISHE", "ASUSE", "GENDER", "NFHS", 
    "ENVSTATS", "RBI", "NSS77", "NSS78", "CPIALRL", "HCES", "TUS"
])
def test_simple_indicators(dataset):
    try:
        result = nsoindia.get_indicators(dataset)
    except (NoDataError, APIError) as exc:
        assert str(exc)
    else:
        assert isinstance(result, (dict, list))
        assert len(result) > 0
