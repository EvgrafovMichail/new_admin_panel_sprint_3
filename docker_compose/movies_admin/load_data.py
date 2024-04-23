from data_transfering.db_tools.save_load_utils import transfer_data
from data_transfering.models.db_models import db_model_mapping

from data_transfering.settings import (
    SQLITE_PATH,
    DB_CONFIG,
    BATCH_SIZE,
)


def main() -> None:
    transfer_data(
        DB_CONFIG,
        SQLITE_PATH,
        db_model_mapping,
        BATCH_SIZE,
    )


if __name__ == "__main__":
    main()
