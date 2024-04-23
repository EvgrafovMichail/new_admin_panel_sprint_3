import os

from pathlib import Path


DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "8000")),
    "options": "-c search_path=public,content",
}

SQLITE_PATH = Path(__file__).resolve().parent / "db.sqlite"

BATCH_SIZE = 100
