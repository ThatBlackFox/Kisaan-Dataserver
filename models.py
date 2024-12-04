from pydantic import BaseModel
from datetime import datetime

class DateModel(BaseModel):
    date: datetime