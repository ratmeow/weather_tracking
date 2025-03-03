from weather.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from weather.locations.schemas import Location
from weather.locations.models import LocationModel, LocationUserModel
from sqlalchemy import select


class LocationDAO:
    pass

    @staticmethod
    @connection(commit=True)
    async def add_location(user_id: int, location_data: Location, session: AsyncSession) -> None:
        location = LocationModel(**location_data.model_dump())
        session.add(location)
        await session.flush()

        location_user_relation = LocationUserModel(user_id=user_id,
                                                   location_id=location.id)

        session.add(location_user_relation)

    @staticmethod
    @connection(commit=True)
    async def delete_location(user_id: int, location_data: Location, session: AsyncSession) -> None:
        location_query = select(LocationModel).filter_by(longitude=location_data.longitude,
                                                    latitude=location_data.latitude)
        location = await session.scalar(location_query)

        loc_user_query = select(LocationUserModel).filter_by(user_id=user_id, location_id=location.id)
        loc_user_relation = await session.scalar(loc_user_query)

        await session.delete(loc_user_relation)
        await session.flush()
        await session.delete(location)

