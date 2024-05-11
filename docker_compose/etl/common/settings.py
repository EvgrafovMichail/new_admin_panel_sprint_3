import os

from common.settings_shemas import ESConnectionSettings, DBConnectionSettings


CONNECTION_CONFIG = DBConnectionSettings()
ELASTIC_CONFIG = ESConnectionSettings()

ELASTIC_HOST = f"http://{ELASTIC_CONFIG.host}:{ELASTIC_CONFIG.port}/"
INDEX_NAME = os.environ.get("INDEX_NAME")
