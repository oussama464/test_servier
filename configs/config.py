import pathlib

SCHEMA_COL_NAMES = ["id", "title", "date", "journal"]
SUPPORTED_FILE_TYPES = [".json", ".csv"]
LANDING_DATA_DIR = pathlib.Path(__file__).parent.parent.joinpath("data/landing")
REFERENTIAL_DRUGS_DIR = pathlib.Path(__file__).parent.parent.joinpath(
    "referential_drugs"
)
STAGING_DATA_DIR = pathlib.Path(__file__).parent.parent.joinpath("data/staging")
