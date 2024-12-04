from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DateModel(BaseModel):
    date: datetime

class Filter(BaseModel):
    crop: Optional[str]
    centre: Optional[str]
    from_date: Optional[datetime]
    to_date: Optional[datetime]