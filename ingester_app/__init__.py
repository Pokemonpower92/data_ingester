from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ingester_app.config import app_config

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config: str = "development"):
    app = Flask(__name__)

    if config:
        app.config.from_object(app_config[config])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    from ingester_app.blueprints.edgar import edgar_blueprint
    app.register_blueprint(edgar_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"ingester_app": app, "db": db}

    return app
