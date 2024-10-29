from geo.db import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# create the database tables if they don't exist
# Users.metadata.create_all(bind=engine)
