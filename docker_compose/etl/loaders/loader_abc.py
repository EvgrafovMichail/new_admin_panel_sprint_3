import abc

from typing import Any


class Loader(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> None:
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type: type, exc_value: str, traceback: Any) -> None:
        pass

    @abc.abstractmethod
    def load_batch(self, batch: list[Any]) -> None:
        pass
