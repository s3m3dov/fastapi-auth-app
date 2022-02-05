from typing import List

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from crud import item as crud_items
from schemas import ItemCreate, Item
from db.utils import get_db

router = APIRouter()


@router.get("/", response_model=List[Item], dependencies=[Depends(get_db)])
def user_items(Authorize: AuthJWT = Depends(), skip: int = 0, limit: int = 100):
    Authorize.jwt_required()
    items = crud_items.get_items(skip=skip, limit=limit)
    return items


@router.post(
    "/{user_id}/create",
    response_model=Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: ItemCreate):
    return crud_items.create_user_item(item=item, user_id=user_id)