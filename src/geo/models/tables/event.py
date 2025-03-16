from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from geo.db import Base

from src.geo.models.tables.pick import Pick

from typing import List

event_pick_table = Table(
    "event_pick_table",
    Base.metadata,
    Column("event_id", ForeignKey("events.id")),
    Column("pick_id", ForeignKey("picks.id")),
    extend_existing=True
)

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    event_time: Mapped[datetime] = mapped_column()
    magnitude: Mapped[float] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    depth: Mapped[float] = mapped_column()
    network_code: Mapped[str] = mapped_column()
    accepted: Mapped[bool] = mapped_column()

    picks: Mapped[List["Pick"]] = relationship("Pick", secondary=event_pick_table)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'











    # TODO корректные отношения с таской


    # id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    # time = Column(DateTime(timezone=True), nullable=False)
    # network = Column(VARCHAR(32), nullable=False)
    # event = Column(VARCHAR(32), nullable=False)
    # magnitude = Column(DOUBLE(), nullable=False)
    # x = Column(DOUBLE(), nullable=False)
    # y = Column(DOUBLE(), nullable=False)
    # z = Column(DOUBLE(), nullable=False)

    # task_id = Column(GUID(), ForeignKey("tasks.id", ondelete="cascade"), nullable=False)
    # task = relationship("Task", back_populates="events")
    # detections = relationship("Detection", back_populates="event")

    # created_at = Column(DateTime(timezone=True), server_default=func.now())