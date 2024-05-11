from typing import Optional, Any

import psycopg2

from psycopg2.extensions import connection as Connection
from psycopg2.extras import DictCursor, DictRow

from common.settings_shemas import DBConnectionSettings
from common.log import EventLogger
from common.backoff import backoff

from extractors.extractor_abc import Extractor


logger = EventLogger("PG-extractor")

BATCH_SIZE = 100


class NoConnectionSettingsSpecifiedError(Exception):
    "Raise when PGExtractor have no connection_setting data"


class NoConnectionSpecifiedError(Exception):
    "Raise when PGExtractor have no connection data"


class PGExtractor(Extractor):
    _connection_settings: dict[str, str | int]
    _connection: Connection | None
    _cursor: DictCursor | None
    _sql_query_cached: str

    def __init__(self) -> None:
        self._connection_settings = {}
        self._connection = None
        self._cursor = None
        self._sql_query_cached = ""

    def __call__(self, connection_settings: DBConnectionSettings) -> "PGExtractor":
        self._connection_settings = connection_settings.model_dump()
        logger.debug(f"save connection settings: {self._connection_settings}")
        return self

    @backoff()
    def __enter__(self) -> None:
        self._connection = self._start_new_connection()

    def __exit__(self, exc_type: type, exc_value: str, traceback: Any) -> None:
        self._connection.close()
        logger.debug("close DB connection")

        self._connection_settings = {}
        self._connection = None
        self._cursor = None
        self._sql_query_cached = ""

    @backoff()
    def extract_batch(
        self,
        sql_query: str,
        batch_size: int = BATCH_SIZE,
        query_parameters: Optional[tuple[Any]] = None,
    ) -> list[DictRow]:
        self._make_connection_healthy()

        if not query_parameters:
            query_parameters = tuple()

        if self._cursor is None or sql_query != self._sql_query_cached:
            self._cursor = self._connection.cursor(cursor_factory=DictCursor)
            self._cursor.execute(sql_query, query_parameters)
            self._sql_query_cached = sql_query

        return self._cursor.fetchmany(size=batch_size)

    def _start_new_connection(self) -> Connection:
        if not self._connection_settings:
            raise NoConnectionSettingsSpecifiedError

        connection = psycopg2.connect(**self._connection_settings)
        logger.debug("open DB connection")

        return connection

    def _make_connection_healthy(self) -> None:
        if self._connection is None:
            raise NoConnectionSpecifiedError

        if 0 < self._connection.closed:
            logger.debug("connection is closed or broken and will be reopened")
            # make sure that broken connection was closed correctly
            self._connection.close()
            self._cursor = None
            self._connection = self._start_new_connection()

        else:
            logger.debug("current connection is healty and will be used as it is")
