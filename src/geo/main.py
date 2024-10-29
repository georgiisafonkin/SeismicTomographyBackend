import logging
from datetime import timedelta, timezone

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError

# imports for authentication
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from geo.models import schemas
from geo.usermodels import User
from geo.userdb import SessionLocal, engine
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


from geo.config import load_env_config
from geo.controllers import (
    task_router, stats_router, geo_router,
)
from geo.controllers.proc import proc_router
from geo.exceptions import (
    APIError,
    handle_api_error,
    handle_404_error,
    handle_pydantic_error
)
from geo.lifespan import LifeSpan
from geo.services.storage import FileStorage
from geo.utils import custom_openapi
from geo.utils.http import HttpProcessor

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Our JWT secret and algorithm
SECRET_KEY = "our_secret_key" # should be replaced for smth automatically generating
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#this stuff should move to other .py file
class UserCreate(BaseModel):
    username: str
    password: str

def get_user_by_username(db: Session, username: str ) -> User:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "complete"

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/register", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return create_user(db=db, user=user)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.UTC) + expires_delta
    else:
        expire = datetime.now(timezone.UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class ApplicationFactory:

    @staticmethod
    def create_app() -> FastAPI:
        config = load_env_config(".env")
        logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)
        app = FastAPI(
            title="GeoService",
            debug=config.DEBUG,
            swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
            root_path="/api" if not config.DEBUG else "",
            docs_url="/api/docs" if config.DEBUG else "/docs",
            redoc_url="/api/redoc" if config.DEBUG else "/redoc",
        )
        app.openapi = lambda: custom_openapi(app)
        getattr(app, "state").config = config
        getattr(app, "state").storage = FileStorage("./storage")
        getattr(app, "state").http_client = HttpProcessor(
            timeout=timedelta(minutes=10).seconds,
            user_agent="aiohttp/3.7.4 (compatible; Geo/0.1.0)",
        )
        if not config.DEBUG:
            logging.getLogger("apscheduler").setLevel(logging.INFO)
            logging.getLogger("aiohttp").setLevel(logging.WARNING)
        lifespan = LifeSpan(app, config)
        app.add_event_handler("startup", lifespan.startup_handler)
        app.add_event_handler("shutdown", lifespan.shutdown_handler)

        logging.debug("Регистрация маршрутов API")
        api_router = APIRouter(prefix="/api/v1" if config.DEBUG else "")
        api_router.include_router(task_router)
        api_router.include_router(proc_router)
        api_router.include_router(geo_router)
        api_router.include_router(stats_router)
        app.include_router(api_router)
        app.include_router(users_router) # TODO add this route by myself

        logging.debug("Регистрация обработчиков исключений")
        app.add_exception_handler(APIError, handle_api_error)
        app.add_exception_handler(404, handle_404_error)
        app.add_exception_handler(RequestValidationError, handle_pydantic_error)

        # some additions for authentication
        oauth2_sceme = OAuth2PasswordBearer(tokenUrl="/token")
        origins = ["http://localhost:3000"]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        logging.info("Приложение успешно создано")
        return app


application = ApplicationFactory.create_app()