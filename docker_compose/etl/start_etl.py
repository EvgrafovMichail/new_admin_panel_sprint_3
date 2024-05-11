import os

from workers.shemas import ETLConnectionsConfig
from workers.etl_process import ETLProcessPG2ES
from common.settings import (
    CONNECTION_CONFIG,
    ELASTIC_CONFIG,
    INDEX_NAME,
)
from common.queries import SQL_QUERIES

from transformers.pg_to_es_transformers import (
    TransformPG2ESFilmwork
)


def main() -> None:
    path_to_states = os.path.join(".", "states")

    if not os.path.exists(path_to_states):
        os.mkdir(path_to_states)

    processes = []

    for i, query in enumerate(SQL_QUERIES):
        connections_config = ETLConnectionsConfig(
            connection_settings_db=CONNECTION_CONFIG,
            connection_settings_es=ELASTIC_CONFIG,
            path_to_state_storage=os.path.join(path_to_states, f"storage_{i}.json"),
            index_name=INDEX_NAME
        )

        processes.append(
            ETLProcessPG2ES(
                transformer=TransformPG2ESFilmwork(),
                connections_config=connections_config,
                sql_query=query,
            )
        )

    for process in processes:
        process.start()


if __name__ == "__main__":
    main()
