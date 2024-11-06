from datetime import datetime

from pydantic import BaseModel


class UserLoginModel(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True

class UserRegisterModel(BaseModel):
    username: str
    password: str
    role: str
    sign_up_date: datetime
    last_login_date: datetime

    class Config:
        from_attributes = True