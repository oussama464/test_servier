from pydantic import BaseModel
import datetime


class ReferencedDrugs(BaseModel):
    drug_name: str
    source_name: str
    source_id: str
    mention_date: datetime.date
    journal: str
    source_file_path: str
    source_file_type: str
    ingestion_timestamp: datetime.datetime = datetime.datetime.now()
    pipeline_owner: str = "ouss@gmail.com"
