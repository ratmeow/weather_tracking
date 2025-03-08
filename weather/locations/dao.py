from sqlalchemy.ext.asyncio import AsyncSession
from weather.locations.schemas import Location
from weather.locations.models import LocationORM, LocationUserORM
from sqlalchemy import select


class LocationDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_location(self, user_id: int, location_data: Location) -> None:
        location = LocationORM(**location_data.model_dump())
        self.db_session.add(location)
        await self.db_session.flush()

        location_user_relation = LocationUserORM(user_id=user_id,
                                                 location_id=location.id)

        self.db_session.add(location_user_relation)

    async def delete_location(self, user_id: int, location_data: Location) -> None:
        location_query = select(LocationORM).filter_by(longitude=location_data.longitude,
                                                       latitude=location_data.latitude)
        location = await self.db_session.scalar(location_query)

        loc_user_query = select(LocationUserORM).filter_by(user_id=user_id, location_id=location.id)
        loc_user_relation = await self.db_session.scalar(loc_user_query)

        await self.db_session.delete(loc_user_relation)
        await self.db_session.flush()
        await self.db_session.delete(location)

    async def get_locations_by_user_id(self, user_id: int) -> list[LocationORM]:
        query = select(LocationORM).join(LocationUserORM, LocationORM.id == LocationUserORM.location_id).filter(
            LocationUserORM.user_id == user_id)
        result = await self.db_session.scalars(query)
        locations = list(result.all())
        return locations
