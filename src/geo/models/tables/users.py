import uuid

from geo.db import Base
from geo.utils.sa import GUID
from sqlalchemy import Column, Integer, String, VARCHAR, DATETIME


class Users(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = Column(VARCHAR(32), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(128), nullable=False)
    role = Column(VARCHAR(32), nullable=False)
    sign_up_date = Column(DATETIME, nullable=False)
    last_login_date = Column(DATETIME, nullable=False)


# create the database tables if they don't exist
# Users.metadata.create_all(bind=engine)
