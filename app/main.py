import csv
import datetime
import json
import pathlib

import click
from pydantic import ValidationError

from app.models.drugs import Drugs
from app.models.pubmed_trials import PubTrial
from app.models.referenced_drugs import ReferencedDrugs
from app.utils.utils import (
    get_raw_data,
    list_files_in_folder,
    save_to_json,
)


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
    pubmed_trial_sources: list[PubTrial], referential_drugs: list[Drugs], pipeline_owner: str
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
                        pipeline_owner=pipeline_owner,
                    ).model_dump()
                )
    return output


@click.group()
def cli():
    """A command-line interface (CLI) group that serves as an entry point for data processing commands."""


@click.command()
@click.argument("landing_data_dir", type=click.Path(exists=True, path_type=pathlib.Path))
@click.argument("staging_data_dir", type=click.Path(exists=False, path_type=pathlib.Path))
@click.argument("referential_drugs_dir", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-o", "--owner", type=str, default="ouss", help="The pipeline owner or the current user of the cli")
def aggregate(
    landing_data_dir: pathlib.Path, staging_data_dir: pathlib.Path, referential_drugs_dir: pathlib.Path, owner: str
):
    """Consolidates data from various sources and saves it to a JSON file."""
    if not staging_data_dir.exists():
        staging_data_dir.mkdir()
    pubmed_trial_sources = get_modeled_data(pathlib.Path(landing_data_dir))
    referential_drugs = get_referential_drugs(pathlib.Path(referential_drugs_dir))
    out_file_name = f"curated_{datetime.datetime.now()}.json"
    output_data = consolidate_data(pubmed_trial_sources, referential_drugs, owner)
    save_to_json(staging_data_dir, output_data, out_file_name)


@click.command()
@click.argument("file_path", type=click.Path(exists=False, path_type=pathlib.Path))
def find_top_journals(file_path: pathlib.Path):
    """Finds the journal that mentions the most unique drugs."""
    journal_count_drugs_map = {}
    with file_path.open(mode="r") as f:
        data = json.load(f)

    unique_drug_journal_pais = set(map(lambda row: (row["drug_name"], row["journal"]), data))
    for _, journal in unique_drug_journal_pais:
        if journal not in journal_count_drugs_map:
            journal_count_drugs_map[journal] = 0
        journal_count_drugs_map[journal] += 1
    max_mentions = max(journal_count_drugs_map.values())
    top_journal_with_most_cited_drugs = {
        journal: count for journal, count in journal_count_drugs_map.items() if count == max_mentions
    }

    click.echo(f"the journal/journals that cite the most unique drugs is/are : {top_journal_with_most_cited_drugs}")


cli.add_command(aggregate)
cli.add_command(find_top_journals)

if __name__ == "__main__":
    cli()
