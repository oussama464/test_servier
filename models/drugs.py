from pydantic import BaseModel


class Drugs(BaseModel):
    atccode: str
    drug: str
