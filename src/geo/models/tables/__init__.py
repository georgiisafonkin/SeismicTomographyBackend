from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from .task import Task
from .station import Station
from .event import Event
from .seisdata import SeisData
from .detection import Detection
from .tomography import Tomography
from .users import UserCreate
