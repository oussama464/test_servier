import datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
)

from app.utils.utils import (
    clean_string,
    parse_date,
)

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
