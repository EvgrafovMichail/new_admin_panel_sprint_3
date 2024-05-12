from typing import Generator, Any

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from common.settings_shemas import ESConnectionSettings
from common.log import EventLogger
from common.backoff import backoff

from loaders.loader_abc import Loader


logger = EventLogger("ES-loader")


class NoElasticsearchHostSpecified(Exception):
    """Raise when ESLoader have no ES host data"""


class NoElasticsearchConnectionSpecified(Exception):
    """Raise when ESLoader have no ES connection data"""


class LostDataError(Exception):
    """Raise when ESLoader fail to load whole batch"""


class ESLoader(Loader):
    _es_client: Elasticsearch | None
    _es_host: str

    def __init__(self) -> None:
        self._es_client = None
        self._es_host = ""

    def __call__(self, connection_settings: ESConnectionSettings) -> "ESLoader":
        self._es_host = (
            f"{connection_settings.scheme}://{connection_settings.host}:"
            f"{connection_settings.port}/"
        )
        logger.debug(f"save ES host: {self._es_host}")

        return self

    @backoff()
    def __enter__(self) -> None:
        if not self._es_host:
            raise NoElasticsearchHostSpecified

        self._es_client = Elasticsearch(self._es_host)
        logger.debug("start new ES connection")

    def __exit__(self, exc_type: type, exc_value: str, traceback: Any) -> None:
        self._es_client.close()
        logger.debug("close ES connection")

        self._es_client = None
        self._es_host = ""

    @backoff()
    def load_batch(
        self,
        batch: list[dict[str, Any]],
        index_name: str,
    ) -> None:
        if self._es_client is None:
            raise NoElasticsearchConnectionSpecified

        batch_sent_size, _ = bulk(
            self._es_client,
            self._get_bulk_batch_generator(batch, index_name),
        )

        if batch_sent_size != len(batch):
            raise LostDataError(
                f"load less data than received: {batch_sent_size} < {len(batch)}"
            )

    @staticmethod
    def _get_bulk_batch_generator(
        data: list[dict[str, Any]],
        index_name: str,
    ) -> Generator[dict[str, Any], None, None]:
        for data_frame in data:
            data_frame["_index"] = index_name

            if (data_id := data_frame.get("id")) is not None:
                data_frame["_id"] = data_id

            yield data_frame
