from fastapi import APIRouter, Depends, Request
from fastapi_jwt_auth import AuthJWT

from celery.result import AsyncResult
from celery_worker import celery as celery_app, user_ip_data_save

from crud import ipdata as crud_ipdata
from schemas.ipdata import IPDataCreate

router = APIRouter()


@router.post('/task/')
def enqueue_user_ip_data(ipdata: IPDataCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    db_ipdata = crud_ipdata.get_by_ip_address(ipdata.ip_address)
    if db_ipdata:
        return {"msg": "The details of this IP exist in the database."}

    task = user_ip_data_save.delay(ipdata.ip_address)
    return {"msg": "Task has been created.", "task_id": task.id}


@router.get("/status/{id}/")
async def check_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"status": result.state}
