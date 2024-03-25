__all__ = ["touch", "Logger", "LogLevel", "create_logger", "bcolors"]
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
    def __lt__(self, other) -> bool: ...

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

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"
