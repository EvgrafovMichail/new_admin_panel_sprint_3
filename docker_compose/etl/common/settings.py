import os

from common.settings_shemas import ElasticSearchSettings, DataBaseSettings


CONNECTION_CONFIG = DataBaseSettings().model_dump()
ELASTIC_CONFIG = ElasticSearchSettings()

ELASTIC_HOST = f"http://{ELASTIC_CONFIG.host}:{ELASTIC_CONFIG.port}/"
INDEX_NAME = os.environ.get("INDEX_NAME")
