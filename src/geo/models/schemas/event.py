from datetime import datetime

from pydantic import BaseModel
from geo.models.schemas.pick import Pick
from typing import List


class Event(BaseModel):
    id: int
    event_time: datetime
    magnitude: float
    latitude: float
    longitude: float
    depth: float
    network_code: str
    accepted: bool
    picks: List[Pick]

    class Config:
        from_attributes = True
