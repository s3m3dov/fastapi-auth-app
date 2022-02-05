from celery import Celery
from celery.utils.log import get_task_logger
from core import settings


celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

logger = get_task_logger(__name__)


@celery.task
def add(x, y):
    res = x + y
    logger.info("Adding %s + %s, res: %s" % (x, y, res))
    return res
