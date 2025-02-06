from src.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from src.locations.models import LocationModel, LocationUserModel
from sqlalchemy import select
from src.locations.schemas import Location
from src.locations.models import LocationModel, LocationUserModel


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
        location = LocationModel(**location_data.model_dump())
        location_user_relation = LocationUserModel(user_id=user_id,
                                                   location_id=location.id)

        await session.delete(location_user_relation)
        await session.delete(location)

