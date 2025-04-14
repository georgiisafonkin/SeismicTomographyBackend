from datetime import datetime

from pydantic import BaseModel


class StationSchema(BaseModel):
    code: str
    latitude: float
    longitude: float
    depth: float
    network_code: str

    class Config:
        from_attributes = True

class StationsRequest(BaseModel):
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float
    network_code: str

    class Config:
        from_attributes = True