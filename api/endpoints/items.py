from typing import List

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

import schemas
import crud
from db.utils import get_db

router = APIRouter()


@router.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def user_items(Authorize: AuthJWT = Depends(), skip: int = 0, limit: int = 100):
    Authorize.jwt_required()
    items = crud.get_items(skip=skip, limit=limit)
    return items
