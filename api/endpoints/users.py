import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from crud import user as crud_user
from schemas import User
from db.utils import get_db

router = APIRouter()
sleep_time = 10


@router.get("/", response_model=List[User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud_user.get_users(skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}", response_model=User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud_user.get_by_id(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get(
    "/slow/", response_model=List[User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    users = crud_user.get_users(skip=skip, limit=limit)
    return users
