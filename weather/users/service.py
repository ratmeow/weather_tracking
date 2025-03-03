from weather.users.dao import UserDAO
from weather.users.schemas import UserSchema, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from weather.auth.utils import get_pwd_hash, verify_pwd
from weather.users.models import UserModel, UserSessionModel
from weather.exceptions import UserAlreadyExistsError, UserNotFoundError, UnauthorizedUserError, UserWrongPasswordError
from datetime import datetime, timedelta, timezone


class UserService:

    @staticmethod
    async def register_user_service(register_data: UserRegisterRequest) -> None:
        user = await UserDAO.get_user_by_login(login=register_data.login)
        if user:
            raise UserAlreadyExistsError(message="User with that login already exists")
        hashed_password = get_pwd_hash(password=register_data.password)
        register_data.password = hashed_password
        await UserDAO.add_user(user_data=register_data)

    @staticmethod
    async def login_user_service(login_data: UserLoginRequest) -> UserSessionResponse:
        user: UserModel = await UserDAO.get_user_by_login(login=login_data.login)
        if user is None:
            raise UserNotFoundError(message="User not found")
        if not verify_pwd(pwd=login_data.password, hashed_pwd=user.password):
            raise UserWrongPasswordError(message="Wrong password")

        user_session = await UserDAO.get_user_session_by_user_id(user_id=user.id)
        if user_session:
            user_session = await UserDAO.update_user_session(user_session=user_session, new_id=True)
        else:
            user_session = await UserDAO.add_user_session(user_id=user.id)

        return UserSessionResponse(session_id=str(user_session.id),
                                   expired_ts=user_session.expired_ts)

    @staticmethod
    async def logout_user_service(session_id: str) -> None:
        return await UserDAO.remove_user_session(session_id=session_id)

    @classmethod
    async def get_user_by_session(cls, session_id: str) -> UserSchema:
        user_session: UserSessionModel = await UserDAO.get_user_session_by_id(session_id=session_id)
        if not user_session or await cls._session_expired_check(user_session=user_session):
            raise UnauthorizedUserError
        await UserDAO.update_user_session(user_session=user_session)
        user = UserSchema.from_orm(user_session.user)
        return user

    @staticmethod
    async def _session_expired_check(user_session: UserSessionModel) -> bool:
        if datetime.now(timezone.utc) > user_session.expired_ts:
            return True
        return False
