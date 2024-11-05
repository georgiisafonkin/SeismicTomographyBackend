from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from geo import services
from geo.models.tables import UserCreate
from geo.services import users, ServiceFactory

from geo.db import get_db
from geo.services.di import get_services
from geo.views.user import UserResponse
from src.geo.models.schemas.users import Users
from geo.services.users import UsersApplicationService, ACCESS_TOKEN_EXPIRE_MINUTES

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/register", response_model=Users)
async def register_user(user: Users, services: ServiceFactory = Depends(get_services)):

    '''

    Регистрация нового пользователя

    '''

    return UserResponse(content= await services.users.register_user(user=user))

@users_router.post("/token", response_model=Users)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UsersApplicationService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token_expires = timedelta(minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UsersApplicationService.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
                                                               )
    return {"access_token": access_token, "token_type": "bearer"}

@users_router.get("/verify-token/{token}", response_model=Users)
async def verify_token(token: str, db: Session = Depends(get_db)):
    UsersApplicationService.verify_token(token=token)
    return {"message": "Token Verified"}
