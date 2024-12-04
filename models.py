from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DateModel(BaseModel):
    date: datetime

class Filter(BaseModel):
    crop: Optional[str] = None
    centre: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None