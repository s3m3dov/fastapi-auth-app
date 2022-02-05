import schemas
from db import models
from core.security import pwd_context, verify_password, get_password_hash


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(obj_in: schemas.UserCreate):
    db_user = models.User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        fullname=obj_in.fullname,
        is_superuser=obj_in.is_superuser,
    )
    db_user.save()
    return db_user


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
