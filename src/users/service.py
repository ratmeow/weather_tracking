from src.users.dao import UserDAO
from src.users.schemas import UserSchema, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from src.locations.schemas import Location
from src.auth.utils import get_pwd_hash, verify_pwd
from src.users.models import UserModel, UserSessionModel


class UserService:

    @staticmethod
    async def register_user_service(register_data: UserRegisterRequest) -> None:
        # проверка что пользователя с таким логином нет
        hashed_password = get_pwd_hash(password=register_data.password)
        await UserDAO.add_user(user_data=UserSchema(login=register_data.login,
                                                    password=hashed_password))

    @staticmethod
    async def login_user_service(login_data: UserLoginRequest) -> UserSessionResponse:
        user: UserModel = await UserDAO.get_user_by_login(login=login_data.login)
        if verify_pwd(pwd=login_data.password, hashed_pwd=user.password):
            user_session = await UserDAO.add_user_session(user_id=user.id)
            return UserSessionResponse(session_id=str(user_session.id))

    @staticmethod
    async def logout_user_service(session_id: str) -> None:
        return await UserDAO.remove_user_session(session_id=session_id)

    @staticmethod
    async def get_user_locations_service(session_id: str) -> list[Location]:
        user_session: UserSessionModel = await UserDAO.get_user_session(session_id=session_id)
        user: UserModel = user_session.user
        locations = user.locations
        return [Location.from_orm(loc) for loc in locations]

