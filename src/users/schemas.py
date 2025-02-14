from pydantic import BaseModel, ConfigDict
from src.locations.schemas import Location


class UserRegisterRequest(BaseModel):
    login: str
    password: str


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserSessionResponse(BaseModel):
    session_id: str


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    password: str
    locations: list[Location]
