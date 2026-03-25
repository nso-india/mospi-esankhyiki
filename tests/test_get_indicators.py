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
    assert "next_step" in result


def test_cpi_indicators():
    result = nsoindia.get_indicators("CPI")
    # CPI returns base years, not indicators
    assert "data" in result or "_note" in result or "error" in result


def test_iip_returns_guidance():
    result = nsoindia.get_indicators("IIP")
    assert "message" in result


def test_wpi_returns_guidance():
    result = nsoindia.get_indicators("WPI")
    assert "message" in result


def test_nas_indicators():
    try:
        result = nsoindia.get_indicators("NAS")
    except (NoDataError, APIError) as exc:
        assert str(exc)
    else:
        assert "data" in result


def test_ec_indicators():
    result = nsoindia.get_indicators("EC")
    assert "data" in result
    assert len(result["data"]) == 3
