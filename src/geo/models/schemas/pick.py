from pydantic import BaseModel
from datetime import datetime

class Pick(BaseModel):
    id: int
    time: datetime
    phase: str
    station_code: str
    
    class Config:
        from_attributes = True