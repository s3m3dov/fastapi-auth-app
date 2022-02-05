from fastapi import APIRouter

from .endpoints import user, tasks

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(tasks.router, tags=["tasks"])
