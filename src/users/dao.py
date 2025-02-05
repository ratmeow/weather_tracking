from src.users.models import UserModel, UserSessionModel
from src.locations.models import LocationModel
from src.users.schemas import UserSchema
from src.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid
from typing import Optional


class UserDAO:

    @staticmethod
    @connection(commit=True)
    async def add_user(user_data: UserSchema, session: AsyncSession) -> UserModel:
        user = UserModel(login=user_data.login,
                         password=user_data.password)
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    @connection()
    async def get_user_by_login(login: str, session: AsyncSession) -> Optional[UserModel]:
        query = select(UserModel).filter(UserModel.login == login)
        result = await session.execute(query)
        user = result.unique().scalar_one_or_none()
        return user

    @staticmethod
    @connection(commit=True)
    async def add_user_session(user_id: int, session: AsyncSession) -> UserSessionModel:
        user_session = UserSessionModel(id=uuid.uuid4(),
                                        user_id=user_id)
        session.add(user_session)
        await session.flush()
        return user_session

    @staticmethod
    @connection()
    async def get_user_session_by_id(session_id: int, session: AsyncSession) -> Optional[UserSessionModel]:
        user_session: UserSessionModel = await session.get(UserSessionModel, session_id)  # pycharm bug
        return user_session

    @staticmethod
    @connection(commit=True)
    async def remove_user_session(session_id: int, session: AsyncSession) -> None:
        user_session = await session.get(UserSessionModel, session_id)
        if user_session:
            await session.delete(user_session)

    @staticmethod
    @connection()
    async def add_user_location():
        pass

    @staticmethod
    @connection
    async def get_user_locations(user_id: int, session: AsyncSession) -> list[LocationModel]:
        query = select(UserModel).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        locations = user.locations
        return locations

    @staticmethod
    @connection()
    async def get_user_session_by_user(user_id: int, session: AsyncSession) -> Optional[UserSessionModel]:
        result = await session.scalars(select(UserSessionModel).filter_by(user_id=user_id))
        user_session = result.first()
        return user_session
