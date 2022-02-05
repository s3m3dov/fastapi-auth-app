from fastapi import APIRouter

from .endpoints import user, basic, users, items

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(basic.router, prefix="/basic", tags=["basic"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
