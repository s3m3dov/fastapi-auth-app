import time
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

import schemas
import crud
from core import settings
from db.utils import get_db

router = APIRouter()
sleep_time = 10


@router.post('/login/')
def login(user_in: schemas.UserLogin, Authorize: AuthJWT = Depends()):
    db_user = crud.authenticate_user(
        email=user_in.email, password=user_in.password
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password!")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = Authorize.create_access_token(
        subject=db_user.email,
        expires_time=access_token_expires,
        algorithm=settings.AUTH_JWT_TOKEN_ALGORITHM
    )
    refresh_token = Authorize.create_refresh_token(
        subject=db_user.email,
        expires_time=refresh_token_expires,
        algorithm=settings.AUTH_JWT_TOKEN_ALGORITHM
    )

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {"msg": "Successfully logged in.", "access_token": access_token}


@router.get('/user/', response_model=schemas.User, dependencies=[Depends(get_db)])
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    auth_user_email = Authorize.get_jwt_subject()
    db_user = crud.get_user_by_email(auth_user_email)

    return db_user


@router.post('/refresh/')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    auth_user_email = Authorize.get_jwt_subject()

    new_access_token = Authorize.create_access_token(subject=auth_user_email)
    Authorize.set_access_cookies(new_access_token)

    return {"msg": "The token has been refreshed.", "access_token": new_access_token}


@router.delete('/logout/')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logged out."}


@router.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user_in: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system!", )
    return crud.create_user(obj_in=user_in)


@router.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get(
    "/slow-users/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    users = crud.get_users(skip=skip, limit=limit)
    return users
