from src.users.dao import UserDAO
from src.users.schemas import UserSchema, UserRegisterRequest, UserLoginRequest, UserSessionResponse
from src.auth.utils import get_pwd_hash, verify_pwd
from src.users.models import UserModel, UserSessionModel
from src.exceptions import UserAlreadyExistsError, UserNotFoundError, UnauthorizedUserError


class UserService:

    @staticmethod
    async def register_user_service(register_data: UserRegisterRequest) -> None:
        user = await UserDAO.get_user_by_login(login=register_data.login)
        if user:
            raise UserAlreadyExistsError(message="User with that login already exists")
        hashed_password = get_pwd_hash(password=register_data.password)
        await UserDAO.add_user(user_data=UserSchema(login=register_data.login,
                                                    password=hashed_password))

    @staticmethod
    async def login_user_service(login_data: UserLoginRequest) -> UserSessionResponse:
        user: UserModel = await UserDAO.get_user_by_login(login=login_data.login)
        if user is None:
            raise UserNotFoundError(message="User not found")
        if verify_pwd(pwd=login_data.password, hashed_pwd=user.password):
            user_session = await UserDAO.get_user_session_by_user_id(user_id=user.id)
            if not user_session:
                user_session = await UserDAO.add_user_session(user_id=user.id)
            return UserSessionResponse(session_id=str(user_session.id))

    @staticmethod
    async def logout_user_service(session_id: str) -> None:
        return await UserDAO.remove_user_session(session_id=session_id)

    @staticmethod
    async def get_user_by_session(session_id: str) -> UserSchema:
        user_session: UserSessionModel = await UserDAO.get_user_session_by_id(session_id=session_id)
        if not user_session:
            raise UnauthorizedUserError

        user = UserSchema.from_orm(user_session.user)
        return user
