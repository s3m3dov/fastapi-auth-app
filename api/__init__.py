from fastapi import APIRouter

from .endpoints import (
    basic,
    items,
    users,
)

api_router = APIRouter()
api_router.include_router(basic.router, tags=["basic"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
