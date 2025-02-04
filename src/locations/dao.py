from src.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from src.locations.models import LocationModel, LocationUserModel
from sqlalchemy import select
class LocationDAO:
    pass

    # @staticmethod
    # @connection
    # async def get_user_locations(user_id: int, session: AsyncSession) -> list[LocationModel]:
    #     query = select(LocationUserModel).filter_by(user_id=user_id)
    #     result = await session.execute(query)
    #     relations: list[LocationUserModel] = list(result.scalars().all())
    #
    #     locations = [relationfor relation in relations]
