
from sqlalchemy import Column, String, Float
from geo.db import Base

class Station(Base):
    __tablename__ = "stations"
    __table_args__ = {'extend_existing': True}

    code = Column(String, primary_key=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    network_code = Column(String, nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
