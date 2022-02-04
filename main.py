import json
import time
from typing import List

import aiohttp
import uvicorn
from environs import Env

# Environment
env = Env()
env.read_env()


from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request
)

from sql_app import (
    crud,
    schemas,
    database,
    models
)
from sql_app.database import db_state_default
from sql_app.utils import json_prettify

database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

app = FastAPI()
sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


# Endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/my-ip")
async def show_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


@app.get("/my-info")
async def slow_route(request: Request):
    client_ip = request.client.host
    ipdata_key = env("IPDATA_API_KEY", default="test")  # Your Key Here
    ipdata_url = f"https://api.ipdata.co/{client_ip}?api-key={ipdata_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(ipdata_url) as response:
            json_dict = await response.json()
    return json_prettify(json_dict)


@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(skip=skip, limit=limit)
    return items


@app.get(
    "/slowusers/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    users = crud.get_users(skip=skip, limit=limit)
    return users


# Run Fast API app
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips='*',
    )
