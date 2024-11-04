import csv
import datetime
import json

import pytest

from app.configs.config import SCHEMA_COL_NAMES
from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial


@pytest.fixture
def sample_pubtrial_data():
    return {
        "id": "123",
        "title": "A Study on Drugs",
        "date": "2020-01-01",
        "journal": "Medical Journal",
        "source": "pubmed",
        "source_file_path": "/path/to/file.csv",
        "source_file_type": "csv",
    }


# Fixture for sample Drugs data
@pytest.fixture
def sample_drugs_data():
    return {
        "atccode": "B01AC06",
        "drug": "Aspirin",
    }


# Fixture for sample ReferencedDrugs data
@pytest.fixture
def sample_referenced_drugs_data():
    return {
        "drug_name": "Aspirin",
        "source_name": "pubmed",
        "source_id": "1",
        "mention_date": "2020-01-01",
        "journal": "Medical Journal",
        "source_file_path": "/path/to/file.csv",
        "source_file_type": "csv",
    }


# Fixture for creating temporary CSV files
@pytest.fixture
def temporary_csv_file(tmp_path):
    def _create_csv_file(filename, fieldnames, rows):
        csv_file = tmp_path / filename
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        with csv_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return csv_file

    return _create_csv_file


# Fixture for creating temporary JSON files
@pytest.fixture
def temporary_json_file(tmp_path):
    def _create_json_file(filename, data):
        json_file = tmp_path / filename
        json_file.parent.mkdir(parents=True, exist_ok=True)
        with json_file.open("w", encoding="utf-8") as f:
            json.dump(data, f)
        return json_file

    return _create_json_file


@pytest.fixture
def sample_pubmed_trial_sources():
    return [
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


@pytest.fixture
def sample_referential_drugs():
    return [
        Drugs(atccode="B01AC06", drug="Aspirin"),
        Drugs(atccode="M01AE01", drug="Ibuprofen"),
    ]


@pytest.fixture
def setup_integration_test(tmp_path, temporary_csv_file):
    # Create temporary landing data directory
    landing_dir = tmp_path / "landing"
    landing_dir.mkdir()
    # Create sample CSV file in landing data directory
    landing_rows = [
        {"id": "1", "title": "Study on Aspirin", "date": "2020-01-01", "journal": "Medical Journal"},
        {"id": "2", "title": "Study on Ibuprofen", "date": "2020-02-01", "journal": "Health Journal"},
    ]
    temporary_csv_file("landing/pubmed.csv", SCHEMA_COL_NAMES, landing_rows)
    # Create temporary referential drugs directory
    drugs_dir = tmp_path / "referential_drugs"
    drugs_dir.mkdir()
    # Create sample drugs CSV file
    drugs_rows = [
        {"atccode": "B01AC06", "drug": "Aspirin"},
        {"atccode": "M01AE01", "drug": "Ibuprofen"},
    ]
    temporary_csv_file("referential_drugs/drugs.csv", ["atccode", "drug"], drugs_rows)
    # Return the paths
    return landing_dir, drugs_dir
