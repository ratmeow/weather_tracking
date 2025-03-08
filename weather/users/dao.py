from weather.users.models import UserORM, UserSessionORM
from weather.users.schemas import UserSchema, UserRegisterRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid
from typing import Optional
from datetime import datetime, timezone, timedelta


class UserDAO:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_user(self, user_data: UserRegisterRequest) -> UserORM:
        user = UserORM(login=user_data.login,
                       password=user_data.password)
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user

    async def get_user_by_login(self, login: str) -> Optional[UserORM]:
        query = select(UserORM).filter(UserORM.login == login)
        result = await self.db_session.execute(query)
        user = result.unique().scalar_one_or_none()
        return user

    async def add_user_session(self, user_id: int) -> UserSessionORM:
        user_session = UserSessionORM(id=uuid.uuid4(),
                                      user_id=user_id,
                                      expired_ts=datetime.now(timezone.utc) + timedelta(hours=3))
        self.db_session.add(user_session)
        await self.db_session.commit()
        await self.db_session.refresh(user_session)
        return user_session

    async def get_user_session_by_id(self, session_id: int) -> Optional[UserSessionORM]:
        user_session: UserSessionORM = await self.db_session.get(UserSessionORM, session_id)  # pycharm bug
        return user_session

    async def update_user_session(self, user_session: UserSessionORM,
                                  new_id: bool = False):
        if new_id:
            user_session.id = uuid.uuid4()

        user_session.expired_ts = datetime.now(timezone.utc) + timedelta(hours=3)
        self.db_session.add(user_session)
        await self.db_session.commit()
        await self.db_session.refresh(user_session)
        return user_session

    async def remove_user_session(self, session_id: int) -> None:
        user_session = await self.db_session.get(UserSessionORM, session_id)
        if user_session:
            await self.db_session.delete(user_session)
        await self.db_session.commit()

    async def get_user_session_by_user_id(self, user_id: int) -> Optional[UserSessionORM]:
        result = await self.db_session.scalars(select(UserSessionORM).filter_by(user_id=user_id))
        user_session = result.first()
        return user_session
