from app.configs.config import SCHEMA_COL_NAMES
from app.main import (
    consolidate_data,
    get_modeled_data,
    get_referential_drugs,
)


def test_get_modeled_data(tmp_path, temporary_csv_file):
    # Create a temporary CSV file in tmp_path
    rows = [{"id": "1", "title": "Title 1", "date": "2020-01-01", "journal": "Journal 1"}]
    temporary_csv_file("test.csv", SCHEMA_COL_NAMES, rows)
    # Test get_modeled_data
    modeled_data = get_modeled_data(tmp_path)
    assert len(modeled_data) == 1
    assert modeled_data[0].id == "1"


def test_get_referential_drugs(tmp_path, temporary_csv_file):
    # Create a temporary drugs CSV file
    rows = [{"atccode": "B01AC06", "drug": "Aspirin"}]
    temporary_csv_file("drugs.csv", ["atccode", "drug"], rows)
    # Test get_referential_drugs
    drugs = get_referential_drugs(tmp_path)
    assert len(drugs) == 1
    assert drugs[0].drug == "Aspirin"


def test_consolidate_data(sample_pubmed_trial_sources, sample_referential_drugs):
    output = consolidate_data(sample_pubmed_trial_sources, sample_referential_drugs)
    assert len(output) == 2
    drug_names = [item["drug_name"] for item in output]
    assert "Aspirin" in drug_names
    assert "Ibuprofen" in drug_names
