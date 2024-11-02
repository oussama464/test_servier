from pydantic import BaseModel, AfterValidator, BeforeValidator
from typing import Annotated
import datetime
from utils.utils import parse_date, clean_string


Date = Annotated[datetime.date, BeforeValidator(parse_date)]
CuratedStr = Annotated[str, AfterValidator(clean_string)]
CuratedId = Annotated[str, BeforeValidator(lambda id: str(id))]


class PubTrial(BaseModel):
    id: CuratedId
    title: CuratedStr
    date: Date
    journal: CuratedStr
    source: str
    source_file_path: str
    source_file_type: str
