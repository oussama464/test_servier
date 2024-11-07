import datetime

from pydantic import BaseModel


class ReferencedDrugs(BaseModel):
    drug_name: str
    source_name: str
    source_id: str
    mention_date: datetime.date
    journal: str
    source_file_path: str
    source_file_type: str
    pipeline_owner: str
    ingestion_timestamp: str = datetime.datetime.now().isoformat()
