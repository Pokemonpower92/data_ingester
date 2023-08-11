from celery.schedules import crontab

from ingester_app.data_ingester_config.cacheconfig import REDIS_URL


class CeleryConfig:
    broker_url = REDIS_URL
    result_backend = REDIS_URL
    result_expires = 3600

    include = ["ingester_app.data_ingester_async.periodic_tasks.tasks"]

    beat_schedule = {
        'update_ticker_mapping_table': {
            'task': 'ingester_app.data_ingester_async.periodic_tasks.tasks.ingest_cik_ticker_mapping',
            'schedule': crontab(hour="*/24"),
        },
        'update_recent_filings_table': {
            'task': 'ingester_app.data_ingester_async.periodic_tasks.tasks.ingest_recent_filings',
            'schedule': crontab(hour="*/24"),
        },
    }
