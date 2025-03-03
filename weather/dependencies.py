from weather.users.dao import UserDAO
from weather.exceptions import UnauthorizedUserError


async def get_user_session(session_id: int):
    user_session = await UserDAO.get_user_session_by_id(session_id=session_id)
    if not user_session:
        raise UnauthorizedUserError
    return user_session
