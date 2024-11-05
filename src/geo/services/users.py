from http.client import HTTPException

from sqlalchemy.orm import Session, AsyncSession, async_sessionmaker
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from geo.exceptions import NotFound
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

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    @staticmethod
    async def get_user_by_username(self, username: str) -> Users:
        # return db.query(UserCreate).filter(UserCreate.username == username).first()
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            user = await users_repo.get(username=username)
        if not user:
            raise NotFound(f"Пользователь с именем {username!r} не найден")
        return UserCreate.model_validate(user)

    @staticmethod
    async def create_user(self, db: Session, user: Users):
        # hashed_password = pwd_context.hash(user.password)
        # db_user = UserCreate(username=user.username, hashed_password=hashed_password, datetime.now())
        # db.add(db_user)
        # db.commit()
        # return "complete"
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            new_user = await users_repo.create(
                username=user.username,
                hashed_password=user.password,
                sign_up_date=datetime.now(timezone.utc),
                # created_at=datetime.datetime.now(tz=datetime.UTC)
            )
        return UserCreate.model_validate(new_user)


    @staticmethod
    async def authenticate_user(self, db: Session, username: str, password: str):
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            user = await users_repo.get(username=username)
            if not user:
                return False
            if not pwd_context.verify(password, user.hashed_password): # TODO почему сравниваем пароль с хешированным паролем
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