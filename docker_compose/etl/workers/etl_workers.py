from multiprocessing import Process
from typing import Any

from etl_utils.pipeline import start_etl_process


class ETLWorker(Process):
    _connection_config: dict[str, Any]
    _elastic_host: str
    _path_to_storage: str
    _index_name: str
    _query: str

    def __init__(
        self,
        connection_config: dict[str, Any],
        path_to_storage: str,
        elastic_host: str,
        index_name: str,
        query: str,
        *args,
        **kwargs,
    ) -> None:
        self._connection_config = connection_config
        self._path_to_storage = path_to_storage
        self._elastic_host = elastic_host
        self._index_name = index_name
        self._query = query

        super().__init__(*args, **kwargs)

    def run(self) -> None:
        start_etl_process(
            self._connection_config,
            self._elastic_host,
            self._path_to_storage,
            self._query,
            self._index_name,
        )
