from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from core import settings
from crud import user as crud_user
from schemas import UserLogin, UserCreate, User
from db.utils import get_db

router = APIRouter()


@router.post("/signup/", response_model=User, dependencies=[Depends(get_db)])
def create_user(user_in: UserCreate):
    db_user = crud_user.get_by_email(email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system!", )
    return crud_user.create(obj_in=user_in)


@router.post('/login/')
def login(user_in: UserLogin, Authorize: AuthJWT = Depends()):
    db_user = crud_user.authenticate(
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


@router.get('/user/', response_model=User, dependencies=[Depends(get_db)])
def user_detail(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    auth_user_email = Authorize.get_jwt_subject()
    db_user = crud_user.get_by_email(auth_user_email)

    return db_user


@router.post('/refresh/')
def refresh_user_token(Authorize: AuthJWT = Depends()):
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


