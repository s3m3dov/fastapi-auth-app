from fastapi import APIRouter, Request

from celery_worker import add
from schemas.tutorial import Numbers

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World!"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/my-ip/")
async def show_user_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


@router.post('/sum/')
def enqueue_add(n: Numbers):
    add.delay(n.x, n.y)
    # We use celery delay method in order to enqueue the
    # task with the given parameters
