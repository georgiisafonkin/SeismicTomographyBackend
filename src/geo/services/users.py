from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from geo.exceptions import AlreadyExists
from geo.models.schemas import UserLoginModel
from geo.repositories.users import UsersRepo
from geo.models.schemas.users import UserRegisterModel
from geo.models.tables.users import UserTable

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

    async def is_there_this_user(self, username: str) -> UserRegisterModel:
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            user = await users_repo.get(username=username)
        if not user:
            return False
        return True

    async def create_user(self, user: UserRegisterModel):
        hashed = pwd_context.hash(user.password)

        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            new_user = await users_repo.create(
                username=user.username,
                hashed_password=hashed,
                role=user.role,
                sign_up_date=user.sign_up_date,
                last_login_date=user.last_login_date,
            )
            print(type(new_user))
        return UserRegisterModel.model_validate(user)

    async def register_user(self, user: UserRegisterModel):
        if await self.is_there_this_user(username=user.username):
            raise AlreadyExists("Пользователь с таким именем уже существует")
        return await self.create_user(user=user)

    async def authenticate_user(self, username: str, password: str):
        async with self._lazy_session() as session:
            users_repo = UsersRepo(session)
            user = await users_repo.get(username=username)
            if not user:
                return False
            if not pwd_context.verify(password, user.hashed_password):
                return False
            return user

    async def login_and_authenticate_user(self, form_data: OAuth2PasswordRequestForm):
        user = await self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"}
                                )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": form_data.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(tz=timezone.utc) + expires_delta
        else:
            expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    def verify_token(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=403, detail="Token is invalid or expire")
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Token is invalid or expire")