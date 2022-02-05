from typing import Optional

from fastapi import Cookie
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_access_token_from_cookie(csrf_access_token: Optional[str] = Cookie(None)):
    return csrf_access_token


async def get_refresh_token_from_cookie(csrf_refresh_token: Optional[str] = Cookie(None)):
    return csrf_refresh_token

