import json

from app.main import (
    consolidate_data,
    get_modeled_data,
    get_referential_drugs,
)
from app.utils.utils import save_to_json


def test_integration(setup_integration_test, tmp_path):
    landing_dir, drugs_dir = setup_integration_test
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
