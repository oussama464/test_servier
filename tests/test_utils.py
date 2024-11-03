import pytest
import datetime
from app.utils.utils import (
    parse_date,
    clean_string,
    get_raw_csv,
    get_raw_json,
    save_to_json,
)
import json
import csv
import tempfile
from app.configs.config import SCHEMA_COL_NAMES


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


def test_get_raw_csv(tmp_path):
    # Create a temporary CSV file
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
    # Test get_raw_csv
    data_iterator = get_raw_csv(csv_file)
    data = list(data_iterator)
    assert len(data) == 1
    assert data[0]["id"] == "1"
    assert data[0]["source"] == "test"


def test_get_raw_json(tmp_path):
    # Create a temporary JSON file
    test_data = [
        {"id": "1", "title": "Title 1", "date": "2020-01-01", "journal": "Journal 1"}
    ]
    json_file = tmp_path / "test.json"
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(test_data, f)
    # Test get_raw_json
    data_iterator = get_raw_json(json_file)
    data = list(data_iterator)
    assert len(data) == 1
    assert data[0]["id"] == "1"
    assert data[0]["source"] == "test"


def test_save_to_json(tmp_path):
    data = [{"key": "value"}]
    output_file_name = "output.json"
    save_to_json(tmp_path, data, output_file_name)
    output_file = tmp_path / output_file_name
    assert output_file.exists()
    with output_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == data
