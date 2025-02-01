from pydantic import BaseModel
from datetime import date

class PeriodBody(BaseModel):
    from_date: date
    to_date: date

class DayBody(BaseModel):
    date: date
