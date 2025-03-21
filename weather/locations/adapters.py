from weather.weather_client.schemas import OpenWeatherLocationResponse, OpenWeatherLocationWeatherResponse
from weather.locations.schemas import LocationResponse, WeatherResponse
from typing import Type, Optional, Protocol
from weather.weather_client.open_weather_client import OpenWeatherClient
from enum import Enum


class MapperType(Enum):
    LOCATION = "location"
    WEATHER = "weather"


class LocationMapper(Protocol):
    def __call__(self, response: dict) -> LocationResponse:
        pass


class WeatherMapper(Protocol):
    def __call__(self, response: dict, **kwargs) -> WeatherResponse:
        pass


class WeatherClientAdapter:
    _registry: dict[Type, dict[MapperType, LocationMapper | WeatherMapper]] = {}

    @classmethod
    def register(cls, client_class: Type, mapper_type: MapperType):
        def wrapper(func: LocationMapper | WeatherMapper) -> LocationMapper | WeatherMapper:
            if client_class not in cls._registry:
                cls._registry[client_class] = {}
            cls._registry[client_class][mapper_type] = func
            return func

        return wrapper

    @classmethod
    def get_location_mapper(cls, client) -> Optional[LocationMapper]:
        return cls._registry.get(type(client), {}).get(MapperType.LOCATION)

    @classmethod
    def get_weather_mapper(cls, client) -> Optional[WeatherMapper]:
        return cls._registry.get(type(client), {}).get(MapperType.WEATHER)


@WeatherClientAdapter.register(client_class=OpenWeatherClient, mapper_type=MapperType.LOCATION)
def map_location_from_open_weather(response: OpenWeatherLocationResponse) -> LocationResponse:
    return LocationResponse(name=response.name,
                            latitude=response.latitude,
                            longitude=response.longitude,
                            country=response.country,
                            state=response.state)


@WeatherClientAdapter.register(client_class=OpenWeatherClient, mapper_type=MapperType.WEATHER)
def map_weather_from_open_weather(name: str, response: OpenWeatherLocationWeatherResponse) -> WeatherResponse:
    return WeatherResponse(name=name,
                           latitude=response.latitude,
                           longitude=response.longitude,
                           country=response.country,
                           temperature=response.temperature,
                           main_weather=response.main_weather,
                           wind_speed=response.wind_speed,
                           temperature_feels=response.temperature_feels,
                           humidity=response.humidity)
