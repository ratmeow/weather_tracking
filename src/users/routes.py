from fastapi import APIRouter, Response, Cookie, Form, HTTPException
from fastapi.responses import RedirectResponse
from typing import Annotated, Optional
from src.users.schemas import UserSchema, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from src.users.service import UserService
from src.locations.service import LocationService
from src.exceptions import UserAlreadyExistsError, DatabaseInternalError, UserNotFoundError
from src.locations.schemas import Location

router = APIRouter(tags=["user"])


@router.post("/register")
async def register_user_api(register_data: UserRegisterRequest):
    try:
        await UserService.register_user_service(register_data=register_data)
        return RedirectResponse(url="/", status_code=303)
    except UserAlreadyExistsError as e:
        return HTTPException(status_code=400, detail=e.message)


@router.post("/login")
async def login_user_api(login_data: UserLoginRequest):
    try:
        user_session = await UserService.login_user_service(login_data=login_data)
        response = RedirectResponse("/", status_code=303)
        response.set_cookie(key="session_id", value=user_session.session_id)
        return response
    except UserNotFoundError as e:
        return HTTPException(status_code=404, detail=e.message)


# поменять на пост
@router.get("/logout")
async def logout_user_api(session_id: Annotated[Optional[str], Cookie()] = None):
    await UserService.logout_user_service(session_id=session_id)
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response


@router.get("/")
async def main_api(session_id: Annotated[Optional[str], Cookie()] = None):
    if session_id:
        return await LocationService.get_locations_by_user_service(session_id=session_id)
    return "Home"


@router.get("/search")
async def location_search_api(location_name: str,
                              session_id: Annotated[Optional[str], Cookie()] = None):
    locations = await LocationService.search_locations_service(location_name=location_name,
                                                               session_id=session_id)
    return locations


@router.post("/search")
async def location_add_api(location_data: Annotated[Location, Form()],
                           session_id: Annotated[Optional[str], Cookie()] = None):
    await LocationService.add_location_service(location_data=location_data,
                                               session_id=session_id)


@router.delete("/")
async def location_delete_api(location_data: Annotated[Location, Form()],
                              session_id: Annotated[Optional[str], Cookie()] = None):
    await LocationService.delete_location_service(location_data=location_data,
                                                  session_id=session_id)
