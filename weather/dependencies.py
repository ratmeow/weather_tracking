from typing import Optional, Annotated

import aiohttp
from fastapi import Depends, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from weather.users.dao import UserDAO
from weather.users.service import UserService
from weather.users.schemas import UserSchema
from weather.locations.dao import LocationDAO
from weather.locations.service import LocationService
from weather.locations.open_weather_service import OpenWeatherAPI
from weather.exceptions import UnauthorizedUserError
from weather.settings import AppSettings
from weather.database import get_session


async def get_db_session(request: Request) -> AsyncSession:
    database = request.app.state.database
    async for session in get_session(database=database):
        yield session


def get_app_settings(request: Request) -> AppSettings:
    return request.app.state.app_settings


async def get_user_dao(db_session: AsyncSession = Depends(get_db_session)):
    return UserDAO(db_session=db_session)


async def get_location_dao(db_session: AsyncSession = Depends(get_db_session)):
    return LocationDAO(db_session=db_session)


async def get_user_service(user_dao: UserDAO = Depends(get_user_dao)):
    return UserService(user_dao=user_dao)


async def get_weather_api_session(request: Request):
    yield request.app.state.weather_api_session


async def get_weather_api_service(api_session: aiohttp.ClientSession = Depends(get_weather_api_session),
                                  settings: AppSettings = Depends(get_app_settings)):
    return OpenWeatherAPI(api_session=api_session,
                          api_key=settings.OPENWEATHER_API_KEY)


async def get_location_service(location_dao: LocationDAO = Depends(get_location_dao),
                               weather_api_service: OpenWeatherAPI = Depends(get_weather_api_service)):
    return LocationService(location_dao=location_dao,
                           weather_api_service=weather_api_service)


async def get_user(session_id: Annotated[Optional[str], Cookie()] = None,
                   user_service: UserService = Depends(get_user_service)) -> UserSchema:
    if not session_id:
        raise UnauthorizedUserError
    user_session = await user_service.get_user_by_session(session_id=session_id)
    return user_session
