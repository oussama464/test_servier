from pydantic import (
    BaseModel,
    Field,
    BeforeValidator,
    field_validator,
    ValidationError,
    AfterValidator,
)
import datetime
import re
import csv
from dateutil.parser import parse
from typing import Any, Iterator, Callable
import pathlib
import json
from typing import Annotated, Type, TypeVar
from pprint import pprint

LANDING_DATA_DIR = pathlib.Path(__file__).parent.parent.joinpath("data/landing")
REFERENTIAL_DRUGS_DIR = pathlib.Path(__file__).parent.parent.joinpath(
    "referential_drugs"
)
STAGING_DATA_DIR = pathlib.Path(__file__).parent.parent.joinpath("data/staging")
COLS = ["id", "title", "date", "journal"]


def list_files_in_folder(folder_path: pathlib.Path):
    return [file for file in folder_path.iterdir() if file.is_file()]


def get_raw_csv(path: pathlib.Path) -> Iterator[dict[str, str]]:
    with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
        data = csv.DictReader(f, fieldnames=COLS)
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
            row = {col: entry.get(col) for col in COLS}
            yield {
                **row,
                "source": path.stem,
                "source_file_path": str(path),
                "source_file_type": "json",
            }


def get_raw_data(path: pathlib.Path) -> Iterator[dict[str, str]]:
    if path.suffix == ".json":
        return get_raw_json(path)
    return get_raw_csv(path)


def parse_date(value: Any) -> datetime.date:
    if isinstance(value, str):
        try:
            return parse(value).date()
        except Exception as ex:
            raise ValueError(str(ex))
    return value


def clean_string(value: str) -> str:
    # Remove hex-encoded sequences
    # encode to ascii and decode to utf8
    clean_string = (
        re.sub(r"\\x[0-9A-Fa-f]{2}", "", value.strip())
        .encode("ascii", errors="ignore")
        .decode("utf-8")
    )
    return clean_string


Date = Annotated[datetime.date, BeforeValidator(parse_date)]
CuratedStr = Annotated[str, AfterValidator(clean_string)]
CuratedId = Annotated[str, BeforeValidator(lambda id: str(id))]


class Drugs(BaseModel):
    atccode: str
    drug: str


class PubTrial(BaseModel):
    id: CuratedId
    title: CuratedStr
    date: Date
    journal: CuratedStr
    source: str
    source_file_path: str
    source_file_type: str


def get_modeled_data(data_dir: pathlib.Path) -> list[PubTrial]:
    models = []
    for file in list_files_in_folder(data_dir):
        for row in get_raw_data(file):
            try:
                models.append(PubTrial.model_validate(row))
            except ValidationError as e:
                print(f"Validation error for row {row} in file {file}: {e}")
                continue  # Skip invalid rows TODO: handle invalid rows

    return models


def get_referential_drugs(ref_dir: pathlib.Path) -> list[Drugs]:
    models = []
    for file in list_files_in_folder(ref_dir):
        with open(file, mode="r", encoding="utf-8") as f:
            data = csv.DictReader(f)
            next(data)
            for entry in data:
                models.append(Drugs(**entry))
    return models


class ReferencedDrugs(BaseModel):
    drug_name: str
    source_name: str
    source_id: str
    mention_date: Date
    journal: CuratedStr
    source_file_path: str
    source_file_type: str
    ingestion_timestamp: datetime.datetime = datetime.datetime.now()
    pipeline_owner: str = "ouss@gmail.com"


def consolidate_data(
    pubmed_trial_sources: list[PubTrial], referential_drugs: list[Drugs]
) -> list[dict[str, str]]:
    output = []
    for ref_drug in referential_drugs:
        for pubmed_trial_source in pubmed_trial_sources:
            if ref_drug.drug.lower() in pubmed_trial_source.title.lower():
                output.append(
                    ReferencedDrugs(
                        drug_name=ref_drug.drug,
                        source_name=pubmed_trial_source.source,
                        source_id=pubmed_trial_source.id,
                        mention_date=pubmed_trial_source.date,
                        journal=pubmed_trial_source.journal,
                        source_file_path=pubmed_trial_source.source_file_path,
                        source_file_type=pubmed_trial_source.source_file_type,
                    ).model_dump()
                )
    return output


def save_to_json(
    data_dir: pathlib.Path, data: list[dict[str, str]], output_file_name: str
) -> None:
    with open(
        data_dir / output_file_name,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, default=str, indent=4)


def main():
    pubmed_trial_sources = get_modeled_data(LANDING_DATA_DIR)
    referential_drugs = get_referential_drugs(REFERENTIAL_DRUGS_DIR)
    out_file_name = f"curated_{datetime.datetime.now}"
    output_data = consolidate_data(pubmed_trial_sources, referential_drugs)
    save_to_json(STAGING_DATA_DIR, output_data, out_file_name)


if __name__ == "__main__":
    main()
