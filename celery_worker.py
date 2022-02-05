from celery import Celery
from celery.utils.log import get_task_logger

from core import settings
from db.models import IPData as model_IPData
from crud.ipdata import get_user_ip_data

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

logger = get_task_logger(__name__)


@celery.task
def user_ip_data_save(ip_address):
    ip_data_obj = model_IPData(
        ip_address=ip_address,
        ip_details=get_user_ip_data(ip_address),
    )
    ip_data_obj.save()

    return ip_data_obj
