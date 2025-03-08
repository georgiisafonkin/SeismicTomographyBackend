from datetime import datetime

from pydantic import BaseModel


class Station(BaseModel):
    code: str
    latitude: float
    longitude: float
    depth: float
    network_code: str

    class Config:
        from_attributes = True
