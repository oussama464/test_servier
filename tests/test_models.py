import pytest
from pydantic import ValidationError

from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial
from app.models.referenced_drugs import ReferencedDrugs
from app.utils.utils import clean_string, parse_date


@pytest.mark.parametrize(
    "input_data",
    [
        {
            "id": "123",
            "title": "A Study on Drugs",
            "date": "2020-01-01",
            "journal": "Medical Journal",
            "source": "pubmed",
            "source_file_path": "/path/to/file.csv",
            "source_file_type": "csv",
        },
        {
            "id": 456,
            "title": "Research on Aspirin",
            "date": "2021-05-10",
            "journal": "Health Journal",
            "source": "pubmed",
            "source_file_path": "/path/to/file.json",
            "source_file_type": "json",
        },
    ],
)
def test_pubtrial_model_valid(input_data):
    pubtrial = PubTrial.model_validate(input_data)
    assert pubtrial.id == str(input_data["id"])
    assert pubtrial.title == clean_string(input_data["title"])
    assert pubtrial.date == parse_date(input_data["date"])
    assert pubtrial.journal == clean_string(input_data["journal"])


@pytest.mark.parametrize(
    "input_data",
    [
        # Missing required field 'id'
        {
            "title": "A Study on Drugs",
            "date": "2020-01-01",
            "journal": "Medical Journal",
            "source": "pubmed",
            "source_file_path": "/path/to/file.csv",
            "source_file_type": "csv",
        },
        # Invalid date format
        {
            "id": "123",
            "title": "A Study on Drugs",
            "date": "invalid date",
            "journal": "Medical Journal",
            "source": "pubmed",
            "source_file_path": "/path/to/file.csv",
            "source_file_type": "csv",
        },
    ],
)
def test_pubtrial_model_invalid(input_data):
    with pytest.raises(ValidationError):
        PubTrial.model_validate(input_data)


@pytest.mark.parametrize(
    "input_data",
    [
        {"atccode": "B01AC06", "drug": "Aspirin"},
        {"atccode": "M01AE01", "drug": "Ibuprofen"},
    ],
)
def test_drugs_model_valid(input_data):
    drug = Drugs(**input_data)
    assert drug.atccode == input_data["atccode"]
    assert drug.drug == input_data["drug"]


@pytest.mark.parametrize(
    "input_data",
    [
        # Missing 'drug' field
        {"atccode": "B01AC06"},
        # Missing 'atccode' field
        {"drug": "Aspirin"},
    ],
)
def test_drugs_model_invalid(input_data):
    with pytest.raises(ValidationError):
        Drugs(**input_data)


@pytest.mark.parametrize(
    "input_data",
    [
        {
            "drug_name": "Aspirin",
            "source_name": "pubmed",
            "source_id": "1",
            "mention_date": "2020-01-01",
            "journal": "Medical Journal",
            "source_file_path": "/path/to/file.csv",
            "source_file_type": "csv",
        },
        {
            "drug_name": "Ibuprofen",
            "source_name": "clinical_trials",
            "source_id": "2",
            "mention_date": "2021-05-10",
            "journal": "Health Journal",
            "source_file_path": "/path/to/file.json",
            "source_file_type": "json",
        },
    ],
)
def test_referenceddrugs_model_valid(input_data):
    referenced_drug = ReferencedDrugs(**input_data)
    assert referenced_drug.drug_name == input_data["drug_name"]
    assert referenced_drug.mention_date == parse_date(input_data["mention_date"])


@pytest.mark.parametrize(
    "input_data",
    [
        # Invalid date
        {
            "drug_name": "Aspirin",
            "source_name": "pubmed",
            "source_id": "1",
            "mention_date": "invalid date",
            "journal": "Medical Journal",
            "source_file_path": "/path/to/file.csv",
            "source_file_type": "csv",
        },
        # Missing 'drug_name' field
        {
            "source_name": "pubmed",
            "source_id": "1",
            "mention_date": "2020-01-01",
            "journal": "Medical Journal",
            "source_file_path": "/path/to/file.csv",
            "source_file_type": "csv",
        },
    ],
)
def test_referenceddrugs_model_invalid(input_data):
    with pytest.raises(ValidationError):
        ReferencedDrugs(**input_data)
