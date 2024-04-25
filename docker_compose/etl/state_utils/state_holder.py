from typing import Hashable, Any

from state_utils.storage import StorageJSON


class State:
    _storage: StorageJSON
    _state_buffer: dict[Hashable, Any]

    def __init__(self, storage: StorageJSON) -> None:
        self._storage = storage
        self._state_buffer = self._storage.load_state()

    def get(self, key: Hashable, default: Any) -> Any:
        return self._state_buffer.get(key, default)

    def set(self, key: Hashable, value: Any) -> None:
        self._state_buffer[key] = value
        self._storage.save_state(self._state_buffer)
