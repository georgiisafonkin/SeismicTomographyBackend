import uuid

from sqlalchemy import Column, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from geo.db import Base
from geo.models.schemas import TaskState, TaskStep
from geo.utils.sa import GUID

from src.geo.models.tables.station import Station
from src.geo.models.tables.seisdata import SeisData
from src.geo.models.tables.tomography import Tomography

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.geo.models.tables.event import Event
else:
    Event = "Event"

class TaskStationTable(Base):
    __tablename__ = "task_station_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[GUID] = mapped_column(ForeignKey("tasks.id"))
    station_code: Mapped[str] = mapped_column(ForeignKey("stations.code"))

class TaskEventTable(Base):
    __tablename__ = "task_event_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[GUID] = mapped_column(ForeignKey("tasks.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    state = Column(Enum(TaskState), default=TaskState.PLAIN, nullable=False)
    step = Column(Enum(TaskStep), nullable=True)


    stations: Mapped[List["Station"]] = relationship(secondary="task_station_table", lazy="selectin", cascade="all, delete")
    events: Mapped[List["Event"]] = relationship(secondary="task_event_table", lazy="selectin", cascade="all, delete")

    seisdata: Mapped[SeisData] = relationship("SeisData", back_populates="task", uselist=False, lazy="selectin")
    tomography: Mapped[Tomography] = relationship("Tomography", back_populates="task", uselist=False, lazy="selectin")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_in = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
