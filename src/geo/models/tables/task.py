import uuid

from sqlalchemy import Column, Enum, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from geo.db import Base
from geo.models.schemas import TaskState, TaskStep
from geo.utils.sa import GUID

from src.geo.models.tables.event import Event
from src.geo.models.tables.station import Station
from typing import List

task_event_table = Table(
    "task_event_table",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id")),
    Column("event_id", ForeignKey("events.id")),
    extend_existing=True
)

task_station_table = Table(
    "task_station_table",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id")),
    Column("station_code", ForeignKey("stations.code")),
    extend_existing=True
)

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    state = Column(Enum(TaskState), default=TaskState.PLAIN, nullable=False)
    step = Column(Enum(TaskStep), nullable=True)


    stations: Mapped[List["Station"]] = relationship("Station", secondary=task_station_table)
    events: Mapped[List["Event"]] = relationship("Event", secondary=task_event_table)

    seisdata = relationship("SeisData", back_populates="task", uselist=False)
    tomography = relationship("Tomography", back_populates="task", uselist=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_in = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
