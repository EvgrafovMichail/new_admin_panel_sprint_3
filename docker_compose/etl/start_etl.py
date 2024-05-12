import os

from workers.etl_init_data import query_transformer_index
from workers.shemas import ETLConnectionsConfig
from workers.etl_process import ETLProcessPG2ES
from common.settings import (
    CONNECTION_CONFIG,
    ELASTIC_CONFIG,
)


def main() -> None:
    path_to_states = os.path.join(".", "states")

    if not os.path.exists(path_to_states):
        os.mkdir(path_to_states)

    processes = []

    for i, query_transform_idx in enumerate(query_transformer_index):
        query, transformer, index = query_transform_idx
        connections_config = ETLConnectionsConfig(
            connection_settings_db=CONNECTION_CONFIG,
            connection_settings_es=ELASTIC_CONFIG,
            path_to_state_storage=os.path.join(path_to_states, f"storage_{i}.json"),
            index_name=index,
        )

        processes.append(
            ETLProcessPG2ES(
                transformer=transformer,
                connections_config=connections_config,
                sql_query=query,
            )
        )

    for process in processes:
        process.start()


if __name__ == "__main__":
    main()
