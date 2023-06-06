from ingester_app import create_app
from ingester_app.data_ingester_async.create_celery_app import create_celery_app

flask_app = create_app()
celery_app = create_celery_app(flask_app)

app = celery_app