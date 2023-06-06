from pathlib import Path

from ingester_app.data_ingester_config.databaseconfig import MYSQL_URI


class AppConfig:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = MYSQL_URI
