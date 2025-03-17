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

class EventRequest(BaseModel):
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float
    network_code: str

    class Config:
        from_attributes = True

class EventsByCoordinates(BaseModel):
    id: int
    event_time: datetime
    magnitude: float
    latitude: float
    longitude: float
    depth: float
    network_code: str
    accepted: bool
    
    class Config:
        from_attributes = True