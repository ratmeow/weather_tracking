from weather.weather_client.schemas import OpenWeatherLocationResponse, OpenWeatherLocationWeatherResponse
from weather.locations.schemas import LocationResponse, WeatherResponse


def map_location_from_open_weather(response: OpenWeatherLocationResponse) -> LocationResponse:
    return LocationResponse(name=response.name,
                            latitude=response.latitude,
                            longitude=response.longitude,
                            country=response.country,
                            state=response.state)


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
