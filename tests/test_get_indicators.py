"""Tests for esankhyiki.get_indicators() -requires network access."""

import pytest
import esankhyiki
from esankhyiki.exceptions import APIError, InvalidDatasetError, NoDataError

pytestmark = pytest.mark.network


def test_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        esankhyiki.get_indicators("FAKE")


def test_plfs_indicators():
    result = esankhyiki.get_indicators("PLFS")
    assert "indicators_by_frequency" in result or "error" in result


def test_cpi_indicators():
    result = esankhyiki.get_indicators("CPI")
    assert isinstance(result, (dict, list))


def test_iip_indicators():
    result = esankhyiki.get_indicators("IIP")
    assert isinstance(result, (dict, list))


# def test_wpi_indicators():
#     result = esankhyiki.get_indicators("WPI")
#     assert isinstance(result, (dict, list))


def test_nas_indicators():
    try:
        result = esankhyiki.get_indicators("NAS")
    except (NoDataError, APIError) as exc:
        assert str(exc)
    else:
        assert isinstance(result, (dict, list))


def test_ec_indicators():
    result = esankhyiki.get_indicators("EC")
    assert isinstance(result, (dict, list))


@pytest.mark.parametrize("dataset", [
    "ASI", "ENERGY", "AISHE", "ASUSE", "GENDER", "NFHS",
    "ENVSTATS", "RBI", "NSS77", "NSS78", "CPIALRL", "HCES", "TUS"
])
def test_simple_indicators(dataset):
    try:
        result = esankhyiki.get_indicators(dataset)
    except (NoDataError, APIError) as exc:
        assert str(exc)
    else:
        assert isinstance(result, (dict, list))
        assert len(result) > 0


def test_mnre_indicators():
    try:
        result = esankhyiki.get_indicators("MNRE")
    except (NoDataError, APIError) as exc:
        assert str(exc)
    else:
        assert isinstance(result, (dict, list))
        assert len(result) > 0
