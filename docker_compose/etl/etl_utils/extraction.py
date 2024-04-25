import datetime

from typing import Union, Generator
from contextlib import contextmanager
from functools import wraps

import psycopg2

from psycopg2.extensions import connection as Connection
from psycopg2.extras import DictCursor, DictRow


END_OF_BATCH = None


@contextmanager
def connect_to_postgresql(
    connection_config: dict[str, Union[str, int]]
) -> Generator[Connection, None, None]:
    connection: Connection = psycopg2.connect(**connection_config)

    try:
        yield connection

    finally:
        connection.close()


def coroutine(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        next(generator)

        return generator

    return wrapper


@coroutine
def batch_recivier(
    connection: Connection,
    sql_querie: str,
    batch_size: int = 100,
) -> Generator[list[DictRow] | None, datetime.datetime, None]:
    cursor = connection.cursor(cursor_factory=DictCursor)

    while date_processed_last := (yield):
        cursor.execute(sql_querie, (date_processed_last,))

        while data_batch := cursor.fetchmany(size=batch_size):
            yield data_batch

        yield END_OF_BATCH
