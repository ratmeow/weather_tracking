import requests
from decimal import Decimal
from weather.locations.schemas import LocationSearchAPIRequest, WeatherSearchAPIRequest
from weather.config import app_settings


class OpenWeatherAPI:
    API_KEY = app_settings.OPENWEATHER_API_KEY
    SEARCH_URL = "http://api.openweathermap.org/geo/1.0/direct"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    async def search_location(cls, location_name: str) -> dict:
        params = LocationSearchAPIRequest(q=location_name,
                                          appid=cls.API_KEY)

        response = requests.get(url=cls.SEARCH_URL, params=params).json()
        return response

    @classmethod
    async def get_weather_by_location(cls,
                                      latitude: Decimal,
                                      longitude: Decimal) -> dict:
        params = WeatherSearchAPIRequest(lat=latitude,
                                         lon=longitude,
                                         appid=cls.API_KEY)

        response = requests.get(url=cls.WEATHER_URL, params=params).json()
        return response
