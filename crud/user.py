from db import models
from schemas import UserCreate
from core.security import verify_password, get_password_hash


def get_by_id(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def create(obj_in: UserCreate):
    db_user = models.User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        fullname=obj_in.fullname,
        is_superuser=obj_in.is_superuser,
    )
    db_user.save()
    return db_user


def authenticate(email: str, password: str):
    user = get_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))