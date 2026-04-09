"""Tests for esankhyiki.list_datasets()"""

import esankhyiki

CORE_DATASETS = [
    "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY",
    "AISHE", "ASUSE", "GENDER", "NFHS", "ENVSTATS", "RBI",
    "NSS77", "NSS78", "CPIALRL", "HCES", "TUS", "EC",
]

OPTIONAL_DATASETS = [
    "NSS79", "UDISE",
]

ALL_EXPECTED_DATASETS = CORE_DATASETS + OPTIONAL_DATASETS


def test_list_datasets_returns_all():
    result = esankhyiki.list_datasets()
    assert "datasets" in result
    assert len(result["datasets"]) in {len(CORE_DATASETS), len(ALL_EXPECTED_DATASETS)}
    assert set(result["datasets"]).issubset(set(ALL_EXPECTED_DATASETS))


def test_list_datasets_has_all_datasets():
    result = esankhyiki.list_datasets()
    datasets = result["datasets"]
    for ds in CORE_DATASETS:
        assert ds in datasets, f"Missing dataset: {ds}"
