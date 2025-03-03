class ServiceError(Exception):
    def __init__(self, message: str = ""):
        self.message = message


class DatabaseInternalError(Exception):
    pass


class UserAlreadyExistsError(ServiceError):
    pass


class UserNotFoundError(ServiceError):
    pass

class UnauthorizedUserError(ServiceError):
    pass

class UserWrongPasswordError(ServiceError):
    pass