import aiohttp # noqa
from fastapi import (
    APIRouter,
    Request,
)

from core import settings
from core.utils import json_prettify

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World!"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/my-ip")
async def show_user_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


@router.get("/my-ip-info")
async def show_user_ip_info(request: Request):
    client_ip = request.client.host
    ipdata_url = f"https://api.ipdata.co/{client_ip}?api-key={settings.IPDATA_API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(ipdata_url) as response:
            json_dict = await response.json()
    return json_prettify(json_dict)
