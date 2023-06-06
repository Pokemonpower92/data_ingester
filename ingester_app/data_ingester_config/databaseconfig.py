import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD", "root")
DB_HOST = os.environ.get("DB_HOST", None)
DB_USER = os.environ.get("DB_USER", None)
DB_PASSWORD = os.environ.get("DB_PASSWORD", None)
DB_PORT = os.environ.get("DB_PORT", None)
DB_NAME = os.environ.get("DB_NAME", None)

if DB_HOST:
    MYSQL_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
else:
    MYSQL_URI = f"sqlite:///{BASE_DIR}/db.sqlite3"
