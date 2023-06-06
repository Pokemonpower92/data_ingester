from flask import Flask

from ingester_app.data_ingester_config.app_config import AppConfig
from ingester_app.data_ingester_db import db


def create_app(config: str = "development"):
    app = Flask(__name__)

    if config:
        app.config.from_object(AppConfig)

    from ingester_app.blueprints.edgar import edgar_blueprint
    app.register_blueprint(edgar_blueprint)

    # set up extensions
    db.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"ingester_app": app, "db": db}

    return app
