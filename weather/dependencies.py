from typing import Optional, Annotated

from fastapi import Depends, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from weather.users.dao import UserDAO
from weather.users.service import UserService
from weather.users.schemas import UserDTO
from weather.locations.dao import LocationDAO
from weather.locations.service import LocationService
from weather.weather_client.open_weather_client import OpenWeatherClient
from weather.exceptions import UnauthorizedUserError
from weather.settings import WeatherClientSettings
from weather.database import get_session
from weather.http_client.base import AsyncHTTPClient
from weather.weather_client.base import WeatherClient


async def get_db_session(request: Request) -> AsyncSession:
    database = request.app.state.database
    async for session in get_session(database=database):
        yield session


def get_weather_api_settings(request: Request) -> WeatherClientSettings:
    return request.app.state.weather_api_settings


async def get_user_dao(db_session: AsyncSession = Depends(get_db_session)):
    return UserDAO(db_session=db_session)


async def get_location_dao(db_session: AsyncSession = Depends(get_db_session)):
    return LocationDAO(db_session=db_session)


async def get_user_service(user_dao: UserDAO = Depends(get_user_dao)):
    return UserService(user_dao=user_dao)


async def get_http_client(request: Request):
    yield request.app.state.http_client


async def get_weather_client(http_client: AsyncHTTPClient = Depends(get_http_client),
                             settings: WeatherClientSettings = Depends(get_weather_api_settings)):
    return OpenWeatherClient(async_client=http_client,
                             settings=settings)


async def get_location_service(location_dao: LocationDAO = Depends(get_location_dao),
                               weather_client: WeatherClient = Depends(get_weather_client)):
    return LocationService(location_dao=location_dao,
                           weather_client=weather_client)


async def get_user(session_id: Annotated[Optional[str], Cookie()] = None,
                   user_service: UserService = Depends(get_user_service)) -> UserDTO:
    if not session_id:
        raise UnauthorizedUserError
    user = await user_service.get_user_by_session(session_id=session_id)
    return user
