from datetime import timedelta
from os import access

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from geo.models.schemas import AccessToken
from geo.services import ServiceFactory

from geo.services.di import get_services
from geo.views.token import AccessTokenResponse
from geo.views.user import UserRegisterResponse, UserLoginResponse
from src.geo.models.schemas.users import UserRegisterModel, UserLoginModel
from geo.services.users import UsersApplicationService, ACCESS_TOKEN_EXPIRE_MINUTES

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegisterModel, services: ServiceFactory = Depends(get_services)):

    '''

    Регистрация нового пользователя

    '''

    return UserRegisterResponse(content= await services.users.register_user(user=user))

@users_router.post("/token", response_model=AccessTokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), services: ServiceFactory = Depends(get_services)):

    '''

    Логин и аутентификация пользователя

    '''

    return AccessTokenResponse(content= await services.users.login_and_authenticate_user(form_data=form_data))

@users_router.get("/verify-token/{token}", response_model=AccessTokenResponse)
async def verify_token(token: str, services: ServiceFactory = Depends(get_services)):

    '''

    Проверка токена

    '''

    return AccessTokenResponse(content= services.users.verify_token(token=token))
