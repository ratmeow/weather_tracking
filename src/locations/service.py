from src.locations.schemas import Location, LocationSearchResponse
class LocationService:

    @staticmethod
    async def search_locations_service(location_name: str) -> list[LocationSearchResponse]:
        pass
        # проверить что сессия есть
        # запрос к апи
        # постобработка в модель

    @staticmethod
    async def add_location_service(location_id: int) -> None:
        pass
        # LocationSearchResponse: запрос апи на конкретную локацию
        # добавление локации в бд LocationSearchResponse -> Location
        # привязка к юзеру