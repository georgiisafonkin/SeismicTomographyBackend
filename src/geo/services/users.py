from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.geo.models.schemas.users import Users
from src.geo.models.tables.users import Users as UserCreate

# Our JWT secret and algorithm
SECRET_KEY = "our_secret_key" # should be replaced for smth automatically generating
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsersApplicationService:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Users:
        return db.query(Users).filter(Users.username == username).first()


    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = Users(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        return "complete"

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(Users).filter(Users.username == username).first()
        if not user:
            return False
        if not pwd_context.verify(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.UTC) + expires_delta
        else:
            expire = datetime.now(timezone.UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt