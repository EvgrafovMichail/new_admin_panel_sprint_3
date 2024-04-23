import sqlite3

from contextlib import contextmanager
from typing import (
    TypeVar,
    Generator,
    Iterator,
    Sequence,
    Union,
)
from sqlite3 import Connection as ConnectionSQLite

import psycopg2

from psycopg2.extras import execute_batch
from psycopg2.extensions import (
    connection as ConnectionPostgres,
    cursor as CursorPostgres,
)

from data_transfering.models.db_models import (
    FilmWork,
    Genre,
    Person,
    GenreFilmWork,
    PersonFilmWork,
)


TableModel = TypeVar(
    "TableModel",
    FilmWork,
    Genre,
    Person,
    GenreFilmWork,
    PersonFilmWork,
)


@contextmanager
def connect_to_sqlite(path_to_db: str) -> Generator[ConnectionSQLite, None, None]:
    connection = sqlite3.connect(path_to_db)
    connection.row_factory = sqlite3.Row

    try:
        yield connection

    finally:
        connection.close()


@contextmanager
def connect_to_postgresql(
    connection_config: dict[str, Union[str, int]]
) -> Generator[ConnectionPostgres, None, None]:
    connection: ConnectionPostgres = psycopg2.connect(**connection_config)

    try:
        yield connection

    finally:
        connection.close()


def save_data_to_postgres(
    cursor: CursorPostgres,
    table_name: str,
    data_to_save: Iterator[TableModel],
    column_names: Sequence[str],
    batch_size: int,
) -> None:
    column_names_str = ", ".join(column_names)
    column_placeholders = ", ".join(["%s"] * len(column_names))

    insert_statement = f"""
    INSERT INTO {table_name} ({column_names_str})
    VALUES ({column_placeholders})
    ON CONFLICT (id) DO NOTHING
    """

    execute_batch(
        cursor,
        insert_statement,
        [record.as_tuple(use_current_time=True) for record in data_to_save],
        page_size=batch_size,
    )


def transfer_data(
    postgres_config: dict[str, Union[str, int]],
    path_to_sqlite: str,
    db_model_mapping: dict[str, type],
    batch_size: int,
) -> None:
    with (
        connect_to_postgresql(postgres_config) as connection_postgres,
        connect_to_sqlite(path_to_sqlite) as connection_sqlite,
    ):
        cursor_postgres = connection_postgres.cursor()
        cursor_sqlite = connection_sqlite.cursor()

        for table_name, data_model in db_model_mapping.items():
            select_statement = f"SELECT * FROM {table_name};"
            cursor_sqlite.execute(select_statement)

            while data_batch := cursor_sqlite.fetchmany(size=batch_size):
                data_batch = [data_model(**dict(record)) for record in data_batch]

                save_data_to_postgres(
                    cursor_postgres,
                    table_name,
                    data_batch,
                    data_model.get_field_names(),
                    batch_size,
                )

            connection_postgres.commit()
