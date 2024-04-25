from etl_utils.pipeline import start_etl_process
from workers.etl_workers import ETLWorker
from common.settings import (
    CONNECTION_CONFIG,
    ELASTIC_HOST,
    INDEX_NAME,
)
from common.queries import SQL_QUERIES


def main() -> None:
    processes = [
        ETLWorker(
            CONNECTION_CONFIG,
            f"storage_{i}.json",
            ELASTIC_HOST,
            INDEX_NAME,
            query,
        )
        for i, query in enumerate(SQL_QUERIES)
    ]

    for process in processes:
        process.start()


if __name__ == "__main__":
    main()
