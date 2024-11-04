import datetime
import json

import pytest

from app.configs.config import SCHEMA_COL_NAMES
from app.utils.utils import (
    clean_string,
    get_raw_csv,
    get_raw_data,
    get_raw_json,
    parse_date,
    save_to_json,
)


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("2020-01-01", datetime.date(2020, 1, 1)),
        ("January 1, 2020", datetime.date(2020, 1, 1)),
        (datetime.date(2020, 1, 1), datetime.date(2020, 1, 1)),
    ],
)
def test_parse_date_valid(input_value, expected_output):
    assert parse_date(input_value) == expected_output


def test_parse_date_invalid():
    input_value = "invalid date"
    with pytest.raises(ValueError):
        parse_date(input_value)


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("Journal of emergency nursing\\xc3\\x28", "Journal of emergency nursing"),
        ("Café", "Caf"),  # Assuming clean_string removes non-ASCII characters
        ("Hello World!", "Hello World!"),
    ],
)
def test_clean_string(input_str, expected_output):
    assert clean_string(input_str) == expected_output


def test_get_raw_csv(temporary_csv_file):
    # Use the fixture to create a temporary CSV file
    rows = [{"id": "1", "title": "Title 1", "date": "2020-01-01", "journal": "Journal 1"}]
    csv_file = temporary_csv_file("test.csv", SCHEMA_COL_NAMES, rows)
    # Test get_raw_csv
    data_iterator = get_raw_csv(csv_file)
    data = list(data_iterator)
    assert len(data) == 1
    assert data[0]["id"] == "1"


def test_get_raw_json(temporary_json_file):
    # Use the fixture to create a temporary JSON file
    data = [{"id": "1", "title": "Title 1", "date": "2020-01-01", "journal": "Journal 1"}]
    json_file = temporary_json_file("test.json", data)
    # Test get_raw_json
    data_iterator = get_raw_json(json_file)
    data = list(data_iterator)
    assert len(data) == 1
    assert data[0]["id"] == "1"


def test_get_raw_data(temporary_csv_file, temporary_json_file):
    # Test with CSV file
    csv_rows = [{"id": "1", "title": "CSV Title", "date": "2020-01-01", "journal": "Journal CSV"}]
    csv_file = temporary_csv_file("test.csv", SCHEMA_COL_NAMES, csv_rows)
    data_iterator = get_raw_data(csv_file)
    data = list(data_iterator)
    assert len(data) == 1
    assert data[0]["title"] == "CSV Title"

    # Test with JSON file
    json_data = [{"id": "2", "title": "JSON Title", "date": "2020-02-01", "journal": "Journal JSON"}]
    json_file = temporary_json_file("test.json", json_data)
    data_iterator = get_raw_data(json_file)
    data = list(data_iterator)
    assert len(data) == 1
    assert data[0]["title"] == "JSON Title"


def test_save_to_json(tmp_path):
    data = [{"key": "value"}]
    output_file_name = "output.json"
    save_to_json(tmp_path, data, output_file_name)
    output_file = tmp_path / output_file_name
    assert output_file.exists()
    with output_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == data
