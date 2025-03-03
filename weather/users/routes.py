from fastapi import APIRouter, Response, Cookie, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from weather.users.schemas import UserSchema, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from weather.users.service import UserService
from weather.locations.service import LocationService
from weather.exceptions import UserAlreadyExistsError, DatabaseInternalError, UserNotFoundError
from weather.locations.schemas import Location

router = APIRouter(tags=["user"])


@router.post("/register")
async def register_user_api(register_data: UserRegisterRequest):
    try:
        await UserService.register_user_service(register_data=register_data)
        return Response(status_code=200)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/login")
async def login_user_api(response: Response, login_data: UserLoginRequest):
    try:
        user_session = await UserService.login_user_service(login_data=login_data)
        response = JSONResponse(content={"username": login_data.login})
        response.set_cookie(
            key="session_id",
            value=user_session.session_id,
            expires=user_session.expired_ts
        )
        return response
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


# поменять на пост
@router.post("/logout")
async def logout_user_api(session_id: Annotated[Optional[str], Cookie()] = None):
    await UserService.logout_user_service(session_id=session_id)
    response = Response(status_code=200)
    response.delete_cookie(key="session_id")
    return response