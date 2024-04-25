import os


CONNECTION_CONFIG = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT", "8000")),
    "options": "-c search_path=public,content",
}

ELASTIC_CONFIG = {
    "host": os.environ.get("ELASTIC_HOST"),
    "port": os.environ.get("ELASTIC_PORT"),
}

ELASTIC_HOST = f"https://{ELASTIC_CONFIG['host']}:{ELASTIC_CONFIG['port']}/"
INDEX_NAME = os.environ.get("INDEX_NAME")

