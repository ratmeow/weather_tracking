from decimal import Decimal
from weather.locations.schemas import LocationSearchAPIRequest, WeatherSearchAPIRequest
import aiohttp
import logging
from weather.exceptions import ServiceError, WeatherAPIError
from weather.settings import WeatherAPISettings

logger = logging.getLogger(__name__)


def weather_api_exception_handler(method):
    async def wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        except aiohttp.ClientResponseError as e:
            logger.error(e)
            raise WeatherAPIError
        except Exception as e:
            logger.error(f"WeatherAPI connection error: {e}")
            raise ServiceError

    return wrapper


class OpenWeatherAPI:

    def __init__(self,
                 api_session: aiohttp.ClientSession,
                 settings: WeatherAPISettings):

        self.settings = settings
        self.api_session = api_session

    @weather_api_exception_handler
    async def search_location(self, location_name: str) -> dict:
        params = LocationSearchAPIRequest(q=location_name,
                                          appid=self.settings.API_KEY)

        async with self.api_session.get(url=self.settings.SEARCH_URL, params=params.model_dump()) as response:
            response.raise_for_status()
            return await response.json()

    @weather_api_exception_handler
    async def get_weather_by_location(self,
                                      latitude: Decimal,
                                      longitude: Decimal) -> dict:
        params = WeatherSearchAPIRequest(lat=latitude,
                                         lon=longitude,
                                         appid=self.settings.API_KEY)

        async with self.api_session.get(url=self.settings.WEATHER_URL, params=params.model_dump()) as response:
            response.raise_for_status()
            return await response.json()
