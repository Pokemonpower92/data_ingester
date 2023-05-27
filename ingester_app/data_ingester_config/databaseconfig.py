import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD", "root")
MYSQL_URI = os.environ.get("MYSQL_URI", f"sqlite:///{BASE_DIR}/db.sqlite3")
