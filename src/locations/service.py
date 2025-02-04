from src.locations.schemas import Location
class LocationService:

    @staticmethod
    async def get_user_locations(user_id: int) -> list[Location]:
        pass