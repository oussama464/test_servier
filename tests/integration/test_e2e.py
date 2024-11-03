import pytest
import tempfile
import datetime
import pathlib
import json
import csv
from typing import Iterator
from pydantic import ValidationError
from app.configs.config import SCHEMA_COL_NAMES
from app.main import get_modeled_data, get_referential_drugs, consolidate_data
from pydantic import ValidationError
from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial
from app.models.referenced_drugs import ReferencedDrugs

from app.utils.utils import save_to_json


def test_integration(tmp_path):
    # Create temporary landing data directory
    landing_dir = tmp_path / "landing"
    landing_dir.mkdir()
    # Create sample CSV file in landing data directory
    csv_file = landing_dir / "pubmed.csv"
    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_COL_NAMES)
        writer.writeheader()
        writer.writerow(
            {
                "id": "1",
                "title": "Study on Aspirin",
                "date": "2020-01-01",
                "journal": "Medical Journal",
            }
        )
        writer.writerow(
            {
                "id": "2",
                "title": "Study on Ibuprofen",
                "date": "2020-02-01",
                "journal": "Health Journal",
            }
        )
    # Create temporary referential drugs directory
    drugs_dir = tmp_path / "referential_drugs"
    drugs_dir.mkdir()
    # Create sample drugs CSV file
    drugs_csv = drugs_dir / "drugs.csv"
    with drugs_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["atccode", "drug"])
        writer.writeheader()
        writer.writerow({"atccode": "B01AC06", "drug": "Aspirin"})
        writer.writerow({"atccode": "M01AE01", "drug": "Ibuprofen"})
    # Run the data processing pipeline
    pubmed_trial_sources = get_modeled_data(landing_dir)
    referential_drugs = get_referential_drugs(drugs_dir)
    output_data = consolidate_data(pubmed_trial_sources, referential_drugs)
    # Save to JSON in a staging directory
    staging_dir = tmp_path / "staging"
    staging_dir.mkdir()
    output_file_name = "curated_data.json"
    save_to_json(staging_dir, output_data, output_file_name)
    # Check that the output file exists and contains expected data
    output_file = staging_dir / output_file_name
    assert output_file.exists()
    with output_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert len(saved_data) == 2
    drug_names = [item["drug_name"] for item in saved_data]
    assert "Aspirin" in drug_names
    assert "Ibuprofen" in drug_names
