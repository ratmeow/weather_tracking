from decimal import Decimal
from .schemas import OpenWeatherLocationSearchRequest, OpenWeatherLocationWeatherRequest, OpenWeatherLocationResponse, \
    OpenWeatherLocationWeatherResponse
import logging
from weather.settings import WeatherClientSettings
from weather.http_client.base import AsyncHTTPClient
from weather.http_client.exceptions import RemoteServerError
from .exceptions import InternalOpenWeatherClientError, OpenWeatherClientResponseError
from .utils import safe_int
from .base import WeatherClient

logger = logging.getLogger(__name__)


class OpenWeatherClient(WeatherClient):

    def __init__(self,
                 async_client: AsyncHTTPClient,
                 settings: WeatherClientSettings):
        self.async_client = async_client
        self.settings = settings

    async def search_location(self, location_name: str) -> list[OpenWeatherLocationResponse]:
        params = OpenWeatherLocationSearchRequest(q=location_name,
                                                  appid=self.settings.API_KEY)

        try:
            response_json = await self.async_client.get(url=self.settings.SEARCH_URL,
                                                        params=params.model_dump())
            return [OpenWeatherLocationResponse(**item) for item in response_json]
        except RemoteServerError:
            raise OpenWeatherClientResponseError
        except Exception as e:
            logger.error(e)
            raise InternalOpenWeatherClientError

    async def get_weather_by_location(self,
                                      latitude: Decimal,
                                      longitude: Decimal) -> OpenWeatherLocationWeatherResponse:
        params = OpenWeatherLocationWeatherRequest(lat=latitude,
                                                   lon=longitude,
                                                   appid=self.settings.API_KEY)

        try:
            response_json = await self.async_client.get(url=self.settings.WEATHER_URL,
                                                        params=params.model_dump())

            system_info = response_json.get("sys", {})
            main_info = response_json.get("main", {})
            wind_info = response_json.get("wind", {})
            desc_info = response_json.get("weather", [{}])[0] if response_json.get("weather") else {}

            weather = OpenWeatherLocationWeatherResponse(latitude=latitude,
                                                         longitude=longitude,
                                                         country=system_info.get("country"),
                                                         main_weather=desc_info.get("main"),
                                                         temperature=safe_int(main_info.get("temp")),
                                                         temperature_feels=safe_int(main_info.get("feels_like")),
                                                         wind_speed=safe_int(wind_info.get("speed")),
                                                         humidity=safe_int(main_info.get("humidity")))

            return weather
        except RemoteServerError:
            raise OpenWeatherClientResponseError
        except Exception as e:
            logger.error(e)
            raise InternalOpenWeatherClientError
