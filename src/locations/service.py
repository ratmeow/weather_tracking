from src.locations.schemas import Location, LocationSearchResponse, LocationWeather
from src.users.service import UserService
from src.locations.dao import LocationDAO
from src.locations.open_weather_service import OpenWeatherAPI


class LocationService:

    @staticmethod
    async def search_locations_service(location_name: str, session_id: str) -> list[LocationSearchResponse]:
        _ = await UserService.get_user_by_session(session_id=session_id)
        response = await OpenWeatherAPI.search_location(location_name=location_name)
        locations = [LocationSearchResponse(**city) for city in response]
        return locations

    @staticmethod
    async def add_location_service(location_data: Location, session_id: str) -> None:
        user = await UserService.get_user_by_session(session_id=session_id)

        await LocationDAO.add_location(user_id=user.id,
                                       location_data=location_data)

    @staticmethod
    async def delete_location_service(location_data: Location, session_id: str) -> None:
        user = await UserService.get_user_by_session(session_id=session_id)

        await LocationDAO.delete_location(user_id=user.id,
                                          location_data=location_data)

    @staticmethod
    async def get_locations_by_user_service(session_id: str) -> list[LocationWeather]:
        user = await UserService.get_user_by_session(session_id=session_id)
        locations = user.locations

        locations_weather = []

        for loc in locations:
            response = await OpenWeatherAPI.get_weather_by_location(latitude=loc.latitude,
                                                                    longitude=loc.longitude)
            locations_weather.append(LocationWeather(name=loc.name,
                                                     country=response["sys"]["country"],
                                                     main_weather=response["weather"][0]["main"],
                                                     temperature=int(response["main"]["temp"]),
                                                     temperature_feels=int(response["main"]["feels_like"]),
                                                     wind_speed=int(response["wind"]["speed"]),
                                                     humidity=response["main"]["humidity"]))
        return locations_weather
