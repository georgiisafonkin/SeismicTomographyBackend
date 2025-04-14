from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped, relationship
from geo.db import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.geo.models.tables.task import Task
else:
    Task = "Task"

class Station(Base):
    __tablename__ = "stations"
    __table_args__ = {'extend_existing': True}

    code = Column(String, primary_key=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    network_code = Column(String, nullable=False)
    
    tasks: Mapped[List["Task"]] = relationship(secondary="task_station_table", back_populates="stations")

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.code}>'
