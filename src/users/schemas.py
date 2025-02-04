from pydantic import BaseModel, ConfigDict


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
    login: str
    password: str
