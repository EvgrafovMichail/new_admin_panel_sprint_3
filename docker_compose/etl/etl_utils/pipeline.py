import datetime

from typing import Any
from time import sleep

from state_utils.storage import StorageJSON
from state_utils.state_holder import State

from backoff_utils.backoff import backoff
from common.log import EventLogger

from etl_utils.transformation import transform_sql_data
from etl_utils.loading import ESDataLoader
from etl_utils.extraction import (
    connect_to_postgresql,
    batch_recivier,
    END_OF_BATCH,
)


logger = EventLogger("etl")


TIME_PAUSE = 5


@backoff()
def start_etl_process(
    connection_config: dict[str, Any],
    elastic_host: str,
    path_to_state_storage: str,
    query: str,
    index_name: str,
) -> None:
    storage = StorageJSON(path_to_state_storage)
    state_holder = State(storage)

    # day before "Train arrival" release
    date_processed_default = str(
        datetime.datetime(
            year=1895,
            month=3,
            day=21,
            tzinfo=datetime.timezone.utc,
        )
    )
    date_processed_key = "date_processed"
    es = ESDataLoader(elastic_host)

    with connect_to_postgresql(connection_config) as connection:
        film_work_receiver = batch_recivier(connection, query)
        data = END_OF_BATCH

        date_processed = state_holder.get(date_processed_key, date_processed_default)

        while True:
            if data:
                date_processed = data[-1]["updated_at"]
                data_transformed = transform_sql_data(data)

                logger.debug(f"etract {len(data_transformed)} from DB")
                es.send_data_to_index(data_transformed, index_name)
                logger.debug(f"process {len(data_transformed)} rows")

                data = next(film_work_receiver)
                continue

            if data is END_OF_BATCH:
                state_holder.set(date_processed_key, str(date_processed))
                logger.debug(f"save date into storage: {str(date_processed)}")
                data = film_work_receiver.send(date_processed)

            if not data:
                logger.debug("no data was found for this request")
                logger.debug(f"pause for {TIME_PAUSE} seconds")
                sleep(TIME_PAUSE)
