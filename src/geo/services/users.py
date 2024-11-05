from http.client import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from geo.exceptions import NotFound, AlreadyExists
from geo.repositories.users import UsersRepo
from geo.models.schemas.users import Users
from geo.models.tables.users import UserCreate

# Our JWT secret and algorithm
SECRET_KEY = "our_secret_key" # should be replaced for smth automatically generating
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsersApplicationService:
    def __init__(
            self,
            lazy_session: async_sessionmaker[AsyncSession],
    ):
        self._lazy_session = lazy_session

    async def is_there_this_user(self, username: str) -> Users:
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            user = await users_repo.get(username=username)
        if not user:
            return False
        return True

    async def create_user(self, db: Session, user: Users):
        # hashed_password = pwd_context.hash(user.password)
        # db_user = UserCreate(username=user.username, hashed_password=hashed_password, datetime.now())
        # db.add(db_user)
        # db.commit()
        # return "complete"

        hashed = pwd_context.hash(user.password)

        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            new_user = await users_repo.create(
                username=user.username,
                hashed_password=hashed,
                sign_up_date=datetime.now(timezone.utc),
                # created_at=datetime.datetime.now(tz=datetime.UTC)
            )
        return UserCreate.model_validate(new_user)

    async def register_user(self, username: str, password: str):
        if self.is_there_this_user:
            raise AlreadyExists("Пользователь с таким именем уже существует")
        return await self.create_user(Users(username=username, password=password, role="default"))

    async def authenticate_user(self, db: Session, username: str, password: str):
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            user = await users_repo.get(username=username)
            if not user:
                return False
            if not pwd_context.verify(password, user.hashed_password):
                return False
            return user
        # user = db.query(UserCreate).filter(UserCreate.username == username).first()
        # if not user:
        #     return False
        # if not pwd_context.verify(password, user.hashed_password):
        #     return False
        # return user

    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.UTC) + expires_delta
        else:
            expire = datetime.now(timezone.UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    @staticmethod
    async def verify_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=403, detail="Token is invalid or expire")
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Token is invalid or expire")