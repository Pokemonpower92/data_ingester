from celery import Celery
from ingester_app.data_ingester_async.celery_config import CeleryConfig

app = Celery(__name__)

app.config_from_object(CeleryConfig)
