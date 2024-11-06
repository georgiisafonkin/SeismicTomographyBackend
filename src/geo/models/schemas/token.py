from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    algorithm: str
    expire_minutes: int

    class Config:
        from_attributes = True