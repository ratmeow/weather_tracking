from decimal import Decimal
from weather.locations.schemas import LocationSearchAPIRequest, WeatherSearchAPIRequest
import logging
from weather.exceptions import ServiceError, WeatherAPIError
from weather.settings import WeatherAPISettings
from weather.http_client.base import AsyncHTTPClient
from weather.http_client.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class OpenWeatherAPI:

    def __init__(self,
                 async_client: AsyncHTTPClient,
                 settings: WeatherAPISettings):
        self.async_client = async_client
        self.settings = settings

    async def search_location(self, location_name: str) -> dict:
        params = LocationSearchAPIRequest(q=location_name,
                                          appid=self.settings.API_KEY)

        try:
            response_json = await self.async_client.get(url=self.settings.SEARCH_URL,
                                                        params=params.model_dump())
            return response_json
        except NotFoundError as e:
            raise e
        except Exception as e:
            logger.error(e)
            raise ServiceError

    async def get_weather_by_location(self,
                                      latitude: Decimal,
                                      longitude: Decimal) -> dict:
        params = WeatherSearchAPIRequest(lat=latitude,
                                         lon=longitude,
                                         appid=self.settings.API_KEY)

        try:
            response_json = await self.async_client.get(url=self.settings.WEATHER_URL,
                                                        params=params.model_dump())
            return response_json
        except NotFoundError as e:
            raise e
        except Exception as e:
            logger.error(e)
            raise ServiceError
