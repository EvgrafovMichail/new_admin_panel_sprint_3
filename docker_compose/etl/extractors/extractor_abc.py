import abc

from typing import Any


class Extractor(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> None:
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type: type, exc_value: str, traceback: Any) -> None:
        pass

    @abc.abstractmethod
    def extract_batch(self, batch_size: int) -> list[Any]:
        pass
