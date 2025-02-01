from pydantic import BaseModel
from datetime import date

class RequestBody(BaseModel):
    from_date: date
    to_date: date
    meta_summary: bool

class DayBody(BaseModel):
    date: date
