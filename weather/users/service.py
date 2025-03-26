from weather.users.schemas import UserDTO, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from weather.auth.utils import get_pwd_hash, verify_pwd
from weather.users.models import UserORM, UserSessionORM
from weather.exceptions import UserAlreadyExistsError, UserNotFoundError, UnauthorizedUserError, UserWrongPasswordError
from datetime import datetime, timedelta, timezone
from weather.users.dao import UserDAO


class UserService:

    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    async def register_user(self, register_data: UserRegisterRequest) -> None:
        user = await self.user_dao.get_by_login(login=register_data.login)
        if user:
            raise UserAlreadyExistsError(message="User with that login already exists")
        hashed_password = get_pwd_hash(password=register_data.password)
        register_data.password = hashed_password
        await self.user_dao.add(user_data=register_data)

    async def login_user(self, login_data: UserLoginRequest) -> UserSessionResponse:
        user: UserORM = await self.user_dao.get_by_login(login=login_data.login)
        if user is None:
            raise UserNotFoundError(message="User not found")
        if not verify_pwd(pwd=login_data.password, hashed_pwd=user.password):
            raise UserWrongPasswordError(message="Wrong password")

        user_session = await self.user_dao.get_session_by_user_id(user_id=user.id)
        if user_session:
            user_session = await self.user_dao.update_session(user_session=user_session, new_id=True)
        else:
            user_session = await self.user_dao.add_session(user_id=user.id)

        return UserSessionResponse(session_id=str(user_session.id),
                                   expired_ts=user_session.expired_ts)

    async def logout_user(self, session_id: str) -> None:
        return await self.user_dao.remove_session(session_id=session_id)

    async def get_user_by_session(self, session_id: str) -> UserDTO:
        user_session: UserSessionORM = await self.user_dao.get_session_by_id(session_id=session_id)
        if not user_session or await self._session_expired_check(user_session=user_session):
            raise UnauthorizedUserError
        await self.user_dao.update_session(user_session=user_session)
        user = UserDTO.from_orm(user_session.user)
        return user

    @staticmethod
    async def _session_expired_check(user_session: UserSessionORM) -> bool:
        if datetime.now(timezone.utc) > user_session.expired_ts:
            return True
        return False
