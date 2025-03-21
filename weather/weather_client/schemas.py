from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional


class OpenWeatherLocationSearchRequest(BaseModel):
    q: str
    appid: str
    limit: int = 5


class OpenWeatherLocationWeatherRequest(BaseModel):
    lat: Decimal
    lon: Decimal
    units: str = "metric"
    appid: str


class OpenWeatherLocationResponse(BaseModel):
    name: str
    latitude: Decimal = Field(alias="lat")
    longitude: Decimal = Field(alias="lon")
    country: Optional[str] = None
    state: Optional[str] = None


class OpenWeatherLocationWeatherResponse(BaseModel):
    latitude: Decimal
    longitude: Decimal
    country: Optional[str]
    temperature: Optional[int]
    main_weather: Optional[str]
    wind_speed: Optional[int]
    temperature_feels: Optional[int]
    humidity: Optional[int]
