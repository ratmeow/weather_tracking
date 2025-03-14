import requests
from decimal import Decimal
from weather.locations.schemas import LocationSearchAPIRequest, WeatherSearchAPIRequest
import aiohttp

class OpenWeatherAPI:

    def __init__(self, api_session, api_key: str):
        self.API_KEY = api_key
        self.SEARCH_URL = "http://api.openweathermap.org/geo/1.0/direct"
        self.WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
        self.api_session = api_session

    async def search_location(self, location_name: str) -> dict:
        params = LocationSearchAPIRequest(q=location_name,
                                          appid=self.API_KEY)

        async with self.api_session.get(url=self.SEARCH_URL, params=params.model_dump()) as response:
            return await response.json()

    async def get_weather_by_location(self,
                                      latitude: Decimal,
                                      longitude: Decimal) -> dict:
        params = WeatherSearchAPIRequest(lat=latitude,
                                         lon=longitude,
                                         appid=self.API_KEY)

        async with self.api_session.get(url=self.WEATHER_URL, params=params.model_dump()) as response:
            return await response.json()
