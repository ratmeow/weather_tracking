from fastapi import APIRouter, Response, Cookie, Form, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from weather.users.schemas import UserDTO, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from weather.users.service import UserService
from weather.exceptions import UserAlreadyExistsError, DatabaseInternalError, UserNotFoundError
from weather.dependencies import get_user_service

router = APIRouter(tags=["user"])


@router.post("/register")
async def register_user_api(register_data: UserRegisterRequest,
                            user_service: UserService = Depends(get_user_service)):
    try:
        await user_service.register_user(register_data=register_data)
        return Response(status_code=200)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/login")
async def login_user_api(login_data: UserLoginRequest,
                         user_service: UserService = Depends(get_user_service)):
    try:
        user_session = await user_service.login_user(login_data=login_data)
        response = JSONResponse(content={"username": login_data.login})
        response.set_cookie(
            key="session_id",
            value=user_session.session_id,
            expires=user_session.expired_ts
        )
        return response
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/logout")
async def logout_user_api(session_id: Annotated[Optional[str], Cookie()] = None,
                          user_service: UserService = Depends(get_user_service)):
    await user_service.logout_user(session_id=session_id)
    response = Response(status_code=200)
    response.delete_cookie(key="session_id")
    return response
