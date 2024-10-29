from datetime import datetime

from pydantic import BaseModel


class Users(BaseModel):
    username: str
    hashed_password: str
    role: str
    sign_up_date: datetime
    last_login_date: datetime

    class Config:
        from_attributes = True