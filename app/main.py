import csv
import datetime
import pathlib

from pydantic import ValidationError

from app.configs.config import LANDING_DATA_DIR, REFERENTIAL_DRUGS_DIR, STAGING_DATA_DIR
from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial
from app.models.referenced_drugs import ReferencedDrugs
from app.utils.utils import get_raw_data, list_files_in_folder, save_to_json


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
            # next(data)
            for entry in data:
                models.append(Drugs(**entry))
    return models


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


def main() -> None:
    pubmed_trial_sources = get_modeled_data(LANDING_DATA_DIR)
    referential_drugs = get_referential_drugs(REFERENTIAL_DRUGS_DIR)
    out_file_name = f"curated_{datetime.datetime.now()}"
    output_data = consolidate_data(pubmed_trial_sources, referential_drugs)
    save_to_json(STAGING_DATA_DIR, output_data, out_file_name)


if __name__ == "__main__":
    main()
