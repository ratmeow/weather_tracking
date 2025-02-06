from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class Location(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    latitude: Decimal
    longitude: Decimal


class LocationSearchResponse(BaseModel):
    name: str
    lat: Decimal
    lon: Decimal
    country: str = None
    state: str = None


class LocationSearchAPIRequest(BaseModel):
    q: str
    appid: str
    limit: int = 5


class WeatherSearchAPIRequest(BaseModel):
    lat: Decimal
    lon: Decimal
    units: str = "metric"
    appid: str


class LocationWeather(BaseModel):
    name: str
    country: str
    temperature: int
    main_weather: str
    wind_speed: int
    temperature_feels: int
    humidity: int
