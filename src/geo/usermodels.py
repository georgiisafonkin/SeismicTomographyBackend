from sqlalchemy import Column, Integer, String
from geo.userdb import Base
from geo.userdb import engine
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    id: int


class Config:
    orm_mode = True  # This allows Pydantic to read data from ORM models


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# create the database tables if they don't exist

User.metadata.create_all(bind=engine)
