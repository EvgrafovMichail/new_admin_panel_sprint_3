from pydantic import BaseModel

from common.settings_shemas import (
    DBConnectionSettings,
    ESConnectionSettings,
)


class ETLConnectionsConfig(BaseModel):
    connection_settings_db: DBConnectionSettings
    connection_settings_es: ESConnectionSettings
    path_to_state_storage: str
    index_name: str
