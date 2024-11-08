import csv
import datetime
import json
import pathlib
import re
from typing import (
    Any,
    Iterator,
)

from dateutil.parser import parse

from app.configs.config import (
    SCHEMA_COL_NAMES,
    SUPPORTED_FILE_TYPES,
)


def list_files_in_folder(folder_path: pathlib.Path) -> list[pathlib.Path]:
    return [file for file in folder_path.iterdir() if file.is_file()]


def get_raw_csv(path: pathlib.Path) -> Iterator[dict[str, str]]:
    with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
        data = csv.DictReader(f, fieldnames=SCHEMA_COL_NAMES)
        next(data)
        for row in data:
            yield {
                **row,
                "source": path.stem,
                "source_file_path": str(path),
                "source_file_type": "csv",
            }


def get_raw_json(path: pathlib.Path) -> Iterator[dict[str, str]]:
    with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
        data = json.load(f)
        for entry in data:
            row = {col: entry.get(col) for col in SCHEMA_COL_NAMES}
            yield {
                **row,
                "source": path.stem,
                "source_file_path": str(path),
                "source_file_type": "json",
            }


def get_raw_data(path: pathlib.Path) -> Iterator[dict[str, str]]:
    if path.suffix not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"file format {path.suffix} not supported, supported formats are {SUPPORTED_FILE_TYPES}")
    if path.suffix == ".json":
        return get_raw_json(path)

    return get_raw_csv(path)


def parse_date(value: Any) -> datetime.date:
    if isinstance(value, str):
        try:
            return parse(value).date()
        except Exception as ex:
            raise ValueError(str(ex)) from ex
    return value


def clean_string(value: str) -> str:
    # Remove hex-encoded sequences
    # encode to ascii and decode to utf8
    clean_string = re.sub(r"\\x[0-9A-Fa-f]{2}", "", value.strip()).encode("ascii", errors="ignore").decode("utf-8")
    return clean_string


def save_to_json(data_dir: pathlib.Path, data: list[dict[str, str]], output_file_name: str) -> None:
    with open(
        data_dir / output_file_name,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, default=str, indent=4)
