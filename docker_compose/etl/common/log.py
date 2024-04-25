import logging
import os

from enum import Enum


class Levels(Enum):
    """
    List of levels available for logging
    """

    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR


class EventLogger(logging.Logger):
    """
    Logger objects with specified logging format

    Create logs in next fromat:
    timestamp | logger_name | level | line | message
    """

    def __init__(
        self, name: str, level: Levels = Levels.debug, path_to_logs: str = ""
    ) -> None:
        if not isinstance(level, Levels):
            raise ValueError(f"unexpected level type: {type(level).__name__}")

        super().__init__(name, level=level.value)

        formatter = logging.Formatter(
            "timestamp=%(asctime)s | logger_name=%(name)s | "
            "level=%(levelname)s | line=%(lineno)d | "
            "message=%(message)s;"
        )

        handler_console = logging.StreamHandler()
        handler_console.setLevel(level.value)
        handler_console.setFormatter(formatter)

        self.setLevel(level.value)
        self.addHandler(handler_console)

        if path_to_logs:
            path_to_folder = os.path.split(path_to_logs)[0]

            if path_to_folder and not os.path.exists(path_to_folder):
                os.makedirs(path_to_folder)

            handler_file = logging.FileHandler(path_to_logs)
            handler_file.setLevel(level.value)
            handler_file.setFormatter(formatter)

            self.addHandler(handler_file)
