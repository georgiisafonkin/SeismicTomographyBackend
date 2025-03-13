from geo.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.geo.models.tables.station import Station

class Pick(Base):
    __tablename__ = "picks"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime] = mapped_column()
    phase: Mapped[str] = mapped_column()
    station_code: Mapped[str] = mapped_column() 

    station: Mapped["Station"] = relationship() # one to many

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'