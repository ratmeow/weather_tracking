from pydantic import BaseModel, ConfigDict
from weather.locations.schemas import Location
from datetime import datetime


class UserRegisterRequest(BaseModel):
    login: str
    password: str


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserSessionResponse(BaseModel):
    session_id: str
    expired_ts: datetime


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    password: str
    locations: list[Location]

