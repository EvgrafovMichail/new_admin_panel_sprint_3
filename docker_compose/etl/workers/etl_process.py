import datetime
import time

from multiprocessing import Process
from typing import Callable

from extractors.extractor_pg import PGExtractor
from state_utils.storage import StorageJSON
from state_utils.state_holder import State
from loaders.loader_es import ESLoader
from common.log import EventLogger

from workers.shemas import ETLConnectionsConfig


logger = EventLogger("ETL-process")


class ETLProcessPG2ES(Process):
    ETL_TIMEOUT: float = 5

    _extractor: PGExtractor
    _transformer: Callable
    _loader: ESLoader
    _state: State
    _connections_config: ETLConnectionsConfig
    _sql_query: str

    def __init__(
        self,
        transformer: Callable,
        connections_config: ETLConnectionsConfig,
        sql_query: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._extractor = PGExtractor()
        self._transformer = transformer
        self._loader = ESLoader()

        storage = StorageJSON(connections_config.path_to_state_storage)
        self._state = State(storage)

        self._connections_config = connections_config
        self._sql_query = sql_query

    def run(self) -> None:
        date_processed_key = "date_processed"
        date_processed = self._state.get(
            date_processed_key,
            str(
                datetime.datetime(
                    year=1895,
                    month=3,
                    day=21,
                    tzinfo=datetime.timezone.utc,
                )
            ),
        )

        query_parameters = (date_processed,)
        data_batch = []

        with (
            self._extractor(self._connections_config.connection_settings_db),
            self._loader(self._connections_config.connection_settings_es),
        ):
            while True:
                data_batch = self._extractor.extract_batch(
                    self._sql_query, query_parameters=query_parameters
                )
                logger.debug(f"extracted batch size: {len(data_batch)}")

                if not data_batch:
                    query_parameters = (date_processed,)
                    self._state.set(date_processed_key, str(date_processed))

                    time.sleep(self.ETL_TIMEOUT)
                    continue

                data_batch_transformed = self._transformer(data_batch)
                self._loader.load_batch(
                    data_batch_transformed,
                    index_name=self._connections_config.index_name,
                )
                date_processed = data_batch[-1]["updated_at"]
