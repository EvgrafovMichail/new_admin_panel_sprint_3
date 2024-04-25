import os

from workers.etl_workers import ETLWorker
from common.settings import (
    CONNECTION_CONFIG,
    ELASTIC_HOST,
    INDEX_NAME,
)
from common.queries import SQL_QUERIES


def main() -> None:
    path_to_states = os.path.join(".", "states")

    if not os.path.exists(path_to_states):
        os.mkdir(path_to_states)

    processes = []

    for i, query in enumerate(SQL_QUERIES):
        path_to_storage = os.path.join(path_to_states, f"storage_{i}.json")
        processes.append(
            ETLWorker(
                CONNECTION_CONFIG,
                path_to_storage,
                ELASTIC_HOST,
                INDEX_NAME,
                query,
            )
        )

    for process in processes:
        process.start()


if __name__ == "__main__":
    main()
