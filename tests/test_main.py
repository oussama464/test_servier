import pytest
import datetime
import json
import csv
import tempfile
from app.configs.config import SCHEMA_COL_NAMES
from app.main import get_modeled_data, get_referential_drugs, consolidate_data
from pydantic import ValidationError
from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial
from app.models.referenced_drugs import ReferencedDrugs


def test_get_modeled_data(tmp_path):
    # Create a temporary directory and CSV file
    csv_file = tmp_path / "test.csv"
    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_COL_NAMES)
        writer.writeheader()
        writer.writerow(
            {
                "id": "1",
                "title": "Title 1",
                "date": "2020-01-01",
                "journal": "Journal 1",
            }
        )
    # Test get_modeled_data
    modeled_data = get_modeled_data(tmp_path)
    assert len(modeled_data) == 1
    assert modeled_data[0].id == "1"


def test_get_referential_drugs(tmp_path):
    # Create a temporary directory and CSV file
    csv_file = tmp_path / "drugs.csv"
    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["atccode", "drug"])
        writer.writeheader()
        writer.writerow({"atccode": "B01AC06", "drug": "Aspirin"})
    # Test get_referential_drugs
    drugs = get_referential_drugs(tmp_path)
    assert len(drugs) == 1
    assert drugs[0].drug == "Aspirin"


def test_consolidate_data():
    # Sample data
    pubmed_trial_sources = [
        PubTrial(
            id="1",
            title="Study on Aspirin",
            date=datetime.date(2020, 1, 1),
            journal="Medical Journal",
            source="pubmed",
            source_file_path="/path/to/file.csv",
            source_file_type="csv",
        ),
        PubTrial(
            id="2",
            title="Study on Ibuprofen",
            date=datetime.date(2020, 2, 1),
            journal="Health Journal",
            source="pubmed",
            source_file_path="/path/to/file.csv",
            source_file_type="csv",
        ),
    ]
    referential_drugs = [
        Drugs(atccode="B01AC06", drug="Aspirin"),
        Drugs(atccode="M01AE01", drug="Ibuprofen"),
    ]
    output = consolidate_data(pubmed_trial_sources, referential_drugs)
    assert len(output) == 2
    drug_names = [item["drug_name"] for item in output]
    assert "Aspirin" in drug_names
    assert "Ibuprofen" in drug_names
