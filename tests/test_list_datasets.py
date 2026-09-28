"""Tests for esankhyiki.list_datasets()"""

import esankhyiki

CORE_DATASETS = [
    "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY", "AISHE", "ASUSE",
    "GENDER", "NFHS", "ENVSTATS", "RBI", "NSS77", "NSS78", "CPIALRL", "HCES",
    "TUS", "EC", "NSS73", "NSS75", "NSS75E", "NSS76", "NSS76C", "NSS79",
    "NSS80", "NSS80C", "UDISE", "MNRE", "ISP", "IRRIGATION", "NSS71",
    "NSS71E", "NSS72", "NSS72T", "NSS74"
]

ALL_EXPECTED_DATASETS = CORE_DATASETS


def test_list_datasets_returns_all():
    result = esankhyiki.list_datasets()
    assert "datasets" in result
    # The number of datasets should be exactly what we expect.
    assert len(result["datasets"]) == len(ALL_EXPECTED_DATASETS)
    # The returned set should be identical to our expected set.
    assert set(result["datasets"]) == set(ALL_EXPECTED_DATASETS)


def test_list_datasets_has_all_datasets():
    result = esankhyiki.list_datasets()
    datasets = result["datasets"]
    for ds in CORE_DATASETS:
        assert ds in datasets, f"Missing dataset: {ds}"
