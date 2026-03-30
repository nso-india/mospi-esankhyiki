"""Tests for esankhyiki.get_metadata() -requires network access."""

import pytest
import esankhyiki
from esankhyiki.exceptions import InvalidDatasetError, InvalidFilterError

pytestmark = pytest.mark.network


def test_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        esankhyiki.get_metadata("FAKE")


def test_plfs_requires_indicator_code():
    with pytest.raises(InvalidFilterError):
        esankhyiki.get_metadata("PLFS")


def test_plfs_metadata():
    result = esankhyiki.get_metadata("PLFS", indicator_code=1, frequency_code=1, year_type_code=1)
    assert "filter_values" in result or "error" in result
    assert isinstance(result, (dict, list))

def test_cpi_metadata():
    result = esankhyiki.get_metadata("CPI", base_year="2024", level="Group", series="Current")
    assert isinstance(result, (dict, list))


def test_iip_metadata():
    result = esankhyiki.get_metadata("IIP", base_year="2011-12", frequency="Annually")
    assert isinstance(result, (dict, list))


def test_wpi_metadata():
    result = esankhyiki.get_metadata("WPI", base_year="2011-12")
    assert isinstance(result, (dict, list))


def test_wpi_metadata():
    result = nsoindia.get_metadata("WPI", base_year="2011-12")
    assert isinstance(result, (dict, list))


def test_ec_metadata():
    result = esankhyiki.get_metadata("EC", indicator_code=1)
    assert isinstance(result, (dict, list))


@pytest.mark.parametrize("dataset", [
    "AISHE", "GENDER", "NFHS", "ENVSTATS", "NSS77", "NSS78", "CPIALRL", "HCES", "TUS"
])
def test_simple_indicator_metadata(dataset):
    try:
        result = esankhyiki.get_metadata(dataset, indicator_code=1)
    except (esankhyiki.exceptions.NoDataError, esankhyiki.exceptions.APIError) as e:
        assert str(e)
    else:
        assert isinstance(result, (dict, list))


def test_asi_metadata():
    result = esankhyiki.get_metadata("ASI", classification_year="2008")
    assert isinstance(result, (dict, list))


def test_nas_metadata():
    result = esankhyiki.get_metadata("NAS", indicator_code=1, base_year="2022-23", series="Current", frequency_code=1)
    assert isinstance(result, (dict, list))


def test_energy_metadata():
    result = esankhyiki.get_metadata("ENERGY", indicator_code=1, use_of_energy_balance_code=1)
    assert isinstance(result, (dict, list))


def test_asuse_metadata():
    result = esankhyiki.get_metadata("ASUSE", indicator_code=1, frequency_code=1)
    assert isinstance(result, (dict, list))


def test_rbi_metadata():
    result = esankhyiki.get_metadata("RBI", sub_indicator_code=1)
    assert isinstance(result, (dict, list))
