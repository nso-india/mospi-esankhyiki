import pytest

import esankhyiki
from esankhyiki.exceptions import APIError, InvalidDatasetError, InvalidFilterError, NoDataError


def test_get_indicators_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        esankhyiki.get_indicators("INVALID_DATASET")


def test_get_metadata_missing_required_indicator_raises():
    with pytest.raises(InvalidFilterError):
        esankhyiki.get_metadata("PLFS")


def test_get_metadata_invalid_integer_filter_raises():
    with pytest.raises(InvalidFilterError):
        esankhyiki.get_metadata("PLFS", indicator_code="bad")


def test_api_errors_raise_for_dict_format(monkeypatch):
    def fake_get_data(dataset_name, params):
        return {"error": "upstream failed", "troubleshooting": "bad gateway"}

    monkeypatch.setattr(esankhyiki, "_client", type("StubClient", (), {"get_data": staticmethod(fake_get_data)})())

    with pytest.raises(APIError, match="upstream failed"):
        esankhyiki.get_data(
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
            format="dict",
        )


def test_no_data_raises_for_dataframe_format(monkeypatch):
    def fake_get_data(dataset_name, params):
        return {
            "data": [],
            "msg": "No Data Found",
            "statusCode": True,
            "troubleshooting": "No rows matched.",
            "suggestion": "Try broader filters.",
        }

    monkeypatch.setattr(esankhyiki, "_client", type("StubClient", (), {"get_data": staticmethod(fake_get_data)})())

    with pytest.raises(NoDataError, match="No Data Found"):
        esankhyiki.get_data(
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
            format="df",
        )
