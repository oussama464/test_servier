import pytest
from pydantic import ValidationError

from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial
from app.models.referenced_drugs import ReferencedDrugs
from app.utils.utils import (
    clean_string,
    parse_date,
)


def test_pubtrial_model_valid(sample_pubtrial_data):
    pubtrial = PubTrial.model_validate(sample_pubtrial_data)
    assert pubtrial.id == str(sample_pubtrial_data["id"])
    assert pubtrial.title == clean_string(sample_pubtrial_data["title"])
    assert pubtrial.date == parse_date(sample_pubtrial_data["date"])
    assert pubtrial.journal == clean_string(sample_pubtrial_data["journal"])


def test_pubtrial_model_invalid():
    invalid_data = {
        "id": "123",
        "title": "A Study on Drugs",
        "date": "invalid date",  # Invalid date
        "journal": "Medical Journal",
        "source": "pubmed",
        "source_file_path": "/path/to/file.csv",
        "source_file_type": "csv",
    }
    with pytest.raises(ValidationError):
        PubTrial.model_validate(invalid_data)


def test_drugs_model_valid(sample_drugs_data):
    drug = Drugs(**sample_drugs_data)
    assert drug.atccode == sample_drugs_data["atccode"]
    assert drug.drug == sample_drugs_data["drug"]


def test_drugs_model_invalid():
    invalid_data = {"atccode": "B01AC06"}  # Missing 'drug' field
    with pytest.raises(ValidationError):
        Drugs(**invalid_data)


def test_referenceddrugs_model_valid(sample_referenced_drugs_data):
    referenced_drug = ReferencedDrugs(**sample_referenced_drugs_data)
    assert referenced_drug.drug_name == sample_referenced_drugs_data["drug_name"]
    assert referenced_drug.mention_date == parse_date(sample_referenced_drugs_data["mention_date"])


def test_referenceddrugs_model_invalid(sample_referenced_drugs_data):
    invalid_data = sample_referenced_drugs_data.copy()
    invalid_data["mention_date"] = "invalid date"  # Invalid date
    with pytest.raises(ValidationError):
        ReferencedDrugs(**invalid_data)
