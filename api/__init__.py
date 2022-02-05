from fastapi import APIRouter

from .endpoints import user, tasks
from .endpoints import tutorial, users, items

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(tasks.router, tags=["tasks"])

api_router.include_router(tutorial.router, prefix="/tutorial", tags=["tutorial"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
