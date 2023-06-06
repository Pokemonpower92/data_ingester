from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ingester_app.data_ingester_async.celery_config import CeleryConfig
from ingester_app.data_ingester_config.databaseconfig import MYSQL_URI


db_session = None


def create_celery_app(flask_app=None) -> Celery:
    celery_app = Celery(__name__)
    celery_app.config_from_object(CeleryConfig)

    TaskBase = celery_app.Task

    from ingester_app.data_ingester_db import db

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                engine = create_engine(MYSQL_URI)
                db_sess = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
                db.session = db_sess

                return TaskBase.__call__(self, *args, **kwargs)


        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            """
            After each Celery task, teardown our db session.

            FMI: https://gist.github.com/twolfson/a1b329e9353f9b575131

            Flask-SQLAlchemy uses create_scoped_session at startup which avoids any setup on a
            per-request basis. This means Celery can piggyback off of this initialization.
            """
            db.session.commit()
            db.session.remove()

    celery_app.Task = ContextTask

    return celery_app
