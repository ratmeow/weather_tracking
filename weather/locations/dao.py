from sqlalchemy.ext.asyncio import AsyncSession
from weather.locations.schemas import LocationDTO
from weather.locations.models import LocationORM, LocationUserORM
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from weather.exceptions import UniqueError


class LocationDAO:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_location(self, location_data: LocationDTO) -> Optional[LocationORM]:
        location = LocationORM(**location_data.model_dump())
        try:
            self.db_session.add(location)
            await self.db_session.flush()
            return location
        except IntegrityError:
            await self.db_session.rollback()
            return None

    async def get_location(self, location_data: LocationDTO) -> LocationORM:
        location_query = select(LocationORM).filter_by(longitude=location_data.longitude,
                                                       latitude=location_data.latitude)
        location = await self.db_session.scalar(location_query)
        return location

    async def add_user_location(self, user_id: int, location_id: int):
        location_user_relation = LocationUserORM(user_id=user_id,
                                                 location_id=location_id)
        try:
            self.db_session.add(location_user_relation)
            await self.db_session.flush()
        except IntegrityError:
            await self.db_session.rollback()
            raise UniqueError("This location already in your collection")

    async def delete_location(self, user_id: int, location_data: LocationDTO) -> None:
        location = await self.get_location(location_data=location_data)

        if location:
            loc_user_query = select(LocationUserORM).filter_by(user_id=user_id,
                                                               location_id=location.id)
            loc_user_relation = await self.db_session.scalar(loc_user_query)

            await self.db_session.delete(loc_user_relation)

    async def get_locations_by_user_id(self, user_id: int) -> list[LocationORM]:
        query = select(LocationORM).join(LocationUserORM, LocationORM.id == LocationUserORM.location_id).filter(
            LocationUserORM.user_id == user_id)
        result = await self.db_session.scalars(query)
        locations = list(result.all())
        return locations
