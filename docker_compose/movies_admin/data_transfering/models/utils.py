from typing import Callable, TypeVar


T = TypeVar("T")


def registrate_model(
    table_name: str,
    mapping: dict[str, type],
) -> Callable[[T], T]:
    def _registrate(obj: T) -> T:
        mapping[table_name] = obj
        return obj

    return _registrate
