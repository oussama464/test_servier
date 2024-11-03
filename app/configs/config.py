import pathlib

SCHEMA_COL_NAMES = ["id", "title", "date", "journal"]
SUPPORTED_FILE_TYPES = [".json", ".csv"]
LANDING_DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "landing"
REFERENTIAL_DRUGS_DIR = (
    pathlib.Path(__file__).parent.parent.parent / "referential_drugs"
)

STAGING_DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "staging"
