"""Tests for esankhyiki.list_datasets()"""

import esankhyiki


def test_list_datasets_returns_all():
    result = esankhyiki.list_datasets()
    assert "datasets" in result
    assert len(result["datasets"]) == 19


def test_list_datasets_has_all_datasets():
    result = esankhyiki.list_datasets()
    datasets = result["datasets"]
    expected = [
        "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY",
        "AISHE", "ASUSE", "GENDER", "NFHS", "ENVSTATS", "RBI",
        "NSS77", "NSS78", "CPIALRL", "HCES", "TUS", "EC",
    ]
    for ds in expected:
        assert ds in datasets, f"Missing dataset: {ds}"
