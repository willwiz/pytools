__all__ = ["touch", "Logger", "LogLevel", "create_logger"]
import enum
import logging
from logging import Logger
from typing import Literal


def touch(file: str) -> None: ...


class LogLevel(enum.Enum):
    NULL = 0
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL


def create_logger(
    logger_name: str = "null",
    level: LogLevel = LogLevel.NULL,
    console: bool = True,
    mode: Literal["a", "w"] = "w",
) -> Logger:
    """
    Method to return a custom logger with the given name and level
    """
    ...
