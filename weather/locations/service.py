from weather.locations.schemas import Location, LocationSearchResponse, LocationWeather
from weather.locations.dao import LocationDAO


class LocationService:

    def __init__(self, location_dao, weather_api_service):
        self.location_dao: LocationDAO = location_dao
        self.weather_api_service = weather_api_service

    async def search_locations_service(self, location_name: str) -> list[LocationSearchResponse]:
        response = await self.weather_api_service.search_location(location_name=location_name)
        locations = [LocationSearchResponse(**city) for city in response]
        return locations

    async def add_location_service(self, location_data: Location, user_id: int) -> None:
        await self.location_dao.add_location(user_id=user_id,
                                             location_data=location_data)

    async def delete_location_service(self, location_data: Location, user_id: int) -> None:
        await self.location_dao.delete_location(user_id=user_id,
                                                location_data=location_data)

    async def get_locations_by_user_service(self, user_id: int) -> list[LocationWeather]:
        locations = await self.location_dao.get_locations_by_user_id(user_id=user_id)
        locations_weather = []

        for loc in locations:
            response = await self.weather_api_service.get_weather_by_location(latitude=loc.latitude,
                                                                              longitude=loc.longitude)
            locations_weather.append(LocationWeather(name=loc.name,
                                                     latitude=loc.latitude,
                                                     longitude=loc.longitude,
                                                     country=response["sys"]["country"],
                                                     main_weather=response["weather"][0]["main"],
                                                     temperature=int(response["main"]["temp"]),
                                                     temperature_feels=int(response["main"]["feels_like"]),
                                                     wind_speed=int(response["wind"]["speed"]),
                                                     humidity=response["main"]["humidity"]))
        return locations_weather
