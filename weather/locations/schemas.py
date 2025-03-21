from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import Optional


class LocationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    latitude: Decimal
    longitude: Decimal


class LocationResponse(LocationDTO):
    country: Optional[str] = None
    state: Optional[str] = None


class WeatherResponse(LocationResponse):
    temperature: Optional[int] = Field(default=None)
    main_weather: Optional[str] = Field(default=None, alias="mainWeather")
    wind_speed: Optional[int] = Field(default=None, alias="windSpeed")
    temperature_feels: Optional[int] = Field(default=None, alias="temperatureFeels")
    humidity: Optional[int] = Field(default=None)
