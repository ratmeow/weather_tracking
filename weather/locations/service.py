from weather.locations.schemas import LocationDTO
from weather.locations.dao import LocationDAO
from weather.weather_client.base import WeatherClient
from weather.locations.schemas import LocationResponse, WeatherResponse
from weather.locations.adapters import WeatherClientAdapter
from weather.exceptions import ServiceError


class LocationService:

    def __init__(self, location_dao, weather_client):
        self.location_dao: LocationDAO = location_dao
        self.weather_client: WeatherClient = weather_client

        self.location_mapper = WeatherClientAdapter.get_location_mapper(client=weather_client)
        self.weather_mapper = WeatherClientAdapter.get_weather_mapper(client=weather_client)
        if not self.location_mapper or not self.weather_mapper:
            raise ServiceError

    async def add_location_service(self, location_data: LocationDTO, user_id: int) -> None:
        location = await self.location_dao.add_location(location_data=location_data)
        if location is None:
            location = await self.location_dao.get_location(location_data=location_data)

        await self.location_dao.add_user_location(user_id=user_id,
                                                  location_id=location.id)

    async def delete_location_service(self, location_data: LocationDTO, user_id: int) -> None:
        await self.location_dao.delete_location(user_id=user_id,
                                                location_data=location_data)

    async def search_locations_service(self, location_name: str) -> list[LocationResponse]:
        response = await self.weather_client.search_location(location_name=location_name)
        locations = [self.location_mapper(response=resp) for resp in response]
        return locations

    async def get_locations_by_user_service(self, user_id: int) -> list[WeatherResponse]:
        locations = await self.location_dao.get_locations_by_user_id(user_id=user_id)
        locations_weather = []

        for loc in locations:
            response = await self.weather_client.get_weather_by_location(latitude=loc.latitude,
                                                                         longitude=loc.longitude)
            weather = self.weather_mapper(name=loc.name, response=response)
            locations_weather.append(weather)

        return locations_weather
