import os
from celery import Celery
from startup.config import settings

REDIS_URL = os.getenv("REDIS_URL", settings.REDIS_URL)
CELERY_BACKEND = os.getenv("CELERY_BACKEND", settings.CELERY_BACKEND)

celery_app = Celery("startup", broker=REDIS_URL, backend=CELERY_BACKEND)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
