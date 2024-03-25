__all__ = ["touch", "Logger", "LogLevel", "create_logger", "bcolors"]
import sys
import enum
import logging
from logging import Logger
from typing import Literal
from pathlib import Path


def touch(file: str):
    Path(file).touch()


class LogLevel(enum.Enum):
    NULL = 0
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL

    def __lt__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.value < other.value
        raise NotImplementedError()


def has_FileHandler(handlers: list[logging.Handler]):
    for handler in handlers:
        if type(handler) == logging.FileHandler:
            return True
    return False


def has_StreamHandler(handlers: list[logging.Handler]):
    for handler in handlers:
        if type(handler) == logging.StreamHandler:
            return True
    return False


def create_logger(
    logger_name: str = "null",
    level: LogLevel = LogLevel.NULL,
    console: bool = True,
    mode: Literal["a", "w"] = "w",
) -> Logger:
    """
    Method to return a custom logger with the given name and level
    """
    # format="%(asctime)s::%(levelname)-8s >> %(module)s-%(lineno)d[%(funcName)s]: %(message)s"
    # datefmt="%y-%m-%d %H:%M:%S"
    format = "%(asctime)s::[%(levelname)-.1s]::%(module)s-%(lineno)d>> %(message)s"
    datefmt = "%y-%m-%d %H:%M"
    log_format = logging.Formatter(fmt=format, datefmt=datefmt)
    if (level is LogLevel.NULL) or logger_name == "null":
        logger = logging.getLogger("null")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.NullHandler())  # read below for reason
        logger.propagate = False
    else:
        if mode == "w":
            open(logger_name, "w").close()
        logger = logging.getLogger(logger_name)
        logger.setLevel(level.value)
        # Creating and adding the file handler
        if not has_FileHandler(logger.handlers):
            file_handler = logging.FileHandler(logger_name, mode="a", encoding="utf-8")
            file_handler.setFormatter(log_format)
            logger.addHandler(file_handler)
    # Creating and adding the console handler
    if console and not has_StreamHandler(logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
    return logger


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
