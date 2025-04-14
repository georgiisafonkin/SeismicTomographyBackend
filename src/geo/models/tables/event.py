from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from geo.db import Base
from src.geo.models.tables.pick import Pick

from src.geo.models.tables.task import TaskEventTable
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.geo.models.tables.task import Task
else:
    Task = "Task"

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime] = mapped_column()
    magnitude: Mapped[float] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    depth: Mapped[float] = mapped_column()
    network_code: Mapped[str] = mapped_column()
    accepted: Mapped[bool] = mapped_column()

    picks: Mapped[List[Pick]] = relationship(lazy="selectin")
    tasks: Mapped[List[Task]] = relationship(secondary="task_event_table", back_populates="events")

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'