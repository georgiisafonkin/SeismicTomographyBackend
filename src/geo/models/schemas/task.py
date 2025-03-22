from datetime import datetime
from enum import Enum
from typing import NewType
from uuid import UUID

from pydantic import BaseModel

from geo.models.schemas.station import StationSchema
from geo.models.schemas.event import Event

from typing import List

class TaskState(Enum):
    PLAIN = 'PLAIN'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    DONE = 'DONE'
    FAILED = 'FAILED'


class TaskStep(Enum):
    SEISDATA = 'SEISDATA'
    TOMOGRAPHY = 'TOMOGRAPHY'


TaskID = NewType('TaskID', UUID)


class Task(BaseModel):
    id: TaskID
    state: TaskState
    step: TaskStep | None

    stations: List[StationSchema]
    events: List[Event]

    created_at: datetime
    completed_in: datetime | None

    # TODO: few models for different requests
    # stations: List[StationSchema]
    # events: List[Event]

    class Config:
        from_attributes = True
