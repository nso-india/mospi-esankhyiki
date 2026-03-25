import pytest

import nsoindia
from nsoindia.exceptions import APIError, InvalidDatasetError, InvalidFilterError, NoDataError


def test_get_indicators_invalid_dataset_raises():
    with pytest.raises(InvalidDatasetError):
        nsoindia.get_indicators("INVALID_DATASET")


def test_get_metadata_missing_required_indicator_raises():
    with pytest.raises(InvalidFilterError):
        nsoindia.get_metadata("PLFS")


def test_get_metadata_invalid_integer_filter_raises():
    with pytest.raises(InvalidFilterError):
        nsoindia.get_metadata("PLFS", indicator_code="bad")


def test_api_errors_raise_for_dict_format(monkeypatch):
    def fake_get_data(dataset_name, params):
        return {"error": "upstream failed", "troubleshooting": "bad gateway"}

    monkeypatch.setattr(nsoindia, "_client", type("StubClient", (), {"get_data": staticmethod(fake_get_data)})())

    with pytest.raises(APIError, match="upstream failed"):
        nsoindia.get_data(
            "PLFS",
            {
                "indicator_code": 1,
                "frequency_code": 1,
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

    monkeypatch.setattr(nsoindia, "_client", type("StubClient", (), {"get_data": staticmethod(fake_get_data)})())

    with pytest.raises(NoDataError, match="No Data Found"):
        nsoindia.get_data(
            "PLFS",
            {
                "indicator_code": 1,
                "frequency_code": 1,
                "year": "2023-24",
                "state_code": 99,
                "gender_code": 3,
                "age_code": 1,
                "sector_code": 3,
            },
            format="df",
        )
