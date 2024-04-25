import json
import os

from typing import Hashable, Any

from common.log import EventLogger


logger = EventLogger("storage")


class StorageJSON:
    _path_to_storage: str

    def __init__(self, path_to_storage: str) -> None:
        if os.path.exists(path_to_storage):
            logger.warning(
                f"file {path_to_storage} already exist and will ve overwrite, "
                "some data might be lost forever"
            )

        self._path_to_storage = path_to_storage

    def save_state(self, state: dict[Hashable, Any]) -> None:
        with open(self._path_to_storage, "w") as file:
            json.dump(state, file, indent=4)

    def load_state(self) -> dict[Hashable, Any]:
        try:
            with open(self._path_to_storage, "r") as file:
                state = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError) as exception:
            logger.error(
                f"exception during state loading: {exception}"
            )
            state = {}

        return state
