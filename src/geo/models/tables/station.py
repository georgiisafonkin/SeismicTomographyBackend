import uuid

from sqlalchemy import Column, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from geo.db import Base
from geo.utils.sa import GUID


class Station(Base):
    __tablename__ = "stations"
    __table_args__ = {'extend_existing': True}

    code = Column(String, primary_key=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    network_code = Column(String, nullable=False)

    # detections = relationship("Detection", back_populates="station")

    # task_id = Column(GUID(), ForeignKey("tasks.id", ondelete="cascade"), nullable=False)
    # task = relationship("Task", back_populates="stations")

    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
