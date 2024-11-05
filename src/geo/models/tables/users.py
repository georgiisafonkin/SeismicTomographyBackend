import uuid

from geo.db import Base
from geo.utils.sa import GUID
from sqlalchemy import Column, VARCHAR, DATETIME


class UserCreate(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} # TODO обязательно понять зачем это

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = Column(VARCHAR(32), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(128), nullable=False)
    role = Column(VARCHAR(32), nullable=False)
    sign_up_date = Column(DATETIME, nullable=False)
    last_login_date = Column(DATETIME, nullable=True)
