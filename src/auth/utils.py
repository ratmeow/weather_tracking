from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_pwd_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_pwd(pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(pwd, hashed_pwd)

