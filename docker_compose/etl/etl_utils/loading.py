from typing import Generator, Any

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from backoff_utils.backoff import backoff


class DataSendingError(Exception):
    pass


class ESDataLoader:
    _elastic_host: str

    def __init__(self, elastic_host: str) -> None:
        self._elastic_host = elastic_host

    @backoff()
    def send_data_to_index(
        self,
        data: list[dict[str, Any]],
        index_name: str,
    ) -> None:
        print(self._elastic_host)
        elastic_client = Elasticsearch(
            self._elastic_host,
            verify_certs=False,
        )
        bulk(
            elastic_client,
            self._get_data_generator(data, index_name),
        )

    @staticmethod
    def _get_data_generator(
        data: list[dict[str, Any]],
        index_name: str,
    ) -> Generator[dict[str, Any], None, None]:
        for data_frame in data:
            data_frame["_index"] = index_name

            if (data_id := data_frame.get("id")) is not None:
                data_frame["_id"] = data_id

            yield data_frame
