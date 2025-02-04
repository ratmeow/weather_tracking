from fastapi import APIRouter, Response, Cookie
from fastapi.responses import RedirectResponse
from typing import Annotated, Optional
from src.users.schemas import UserSchema, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from src.users.service import UserService

router = APIRouter(tags=["user"])


@router.post("/register")
async def register_user_api(register_data: UserRegisterRequest):
    await UserService.register_user_service(register_data=register_data)
    return "Success registration"
    # редирект на главную


@router.post("/login")
async def login_user_api(response: Response, login_data: UserLoginRequest):
    user_session = await UserService.login_user_service(login_data=login_data)
    response.set_cookie(key="session_id", value=user_session.session_id)
    return RedirectResponse("/", status_code=303)


@router.get("/logout")
async def logout_user_api(response: Response, session_id: Annotated[Optional[str], Cookie()] = None):
    await UserService.logout_user_service(session_id=session_id)
    response.delete_cookie(key="session_id")
    return "Logout"
# из-за редиректа кука не удаляется


@router.get("/")
async def main_api(session_id: Annotated[Optional[str], Cookie()] = None):
    if session_id:
        return await UserService.get_user_locations_service(session_id=session_id)
    return "Home"
