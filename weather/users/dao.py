from weather.users.models import UserModel, UserSessionModel
from weather.users.schemas import UserSchema, UserRegisterRequest
from weather.database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid
from typing import Optional
from datetime import datetime, timezone, timedelta


class UserDAO:

    @staticmethod
    @connection(commit=True)
    async def add_user(user_data: UserRegisterRequest, session: AsyncSession) -> UserModel:
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
                                        user_id=user_id,
                                        expired_ts=datetime.now(timezone.utc) + timedelta(hours=3))
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
    async def update_user_session(user_session: UserSessionModel,
                                  session: AsyncSession,
                                  new_id: bool = False):
        if new_id:
            user_session.id = uuid.uuid4()

        user_session.expired_ts = datetime.now(timezone.utc) + timedelta(hours=3)
        session.add(user_session)
        await session.flush()
        return user_session

    @staticmethod
    @connection(commit=True)
    async def remove_user_session(session_id: int, session: AsyncSession) -> None:
        user_session = await session.get(UserSessionModel, session_id)
        if user_session:
            await session.delete(user_session)

    @staticmethod
    @connection()
    async def get_user_session_by_user_id(user_id: int, session: AsyncSession) -> Optional[UserSessionModel]:
        result = await session.scalars(select(UserSessionModel).filter_by(user_id=user_id))
        user_session = result.first()
        return user_session
