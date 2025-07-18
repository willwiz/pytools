from __future__ import annotations

__all__ = ["LOG_LEVEL", "ILogger", "LogLevel"]
import abc
import enum
from typing import Literal

type LOG_LEVEL = Literal["NULL", "FATAL", "ERROR", "WARN", "BRIEF", "INFO", "DEBUG"]


class LogLevel(enum.IntEnum):
    NULL = 0
    FATAL = 1
    ERROR = 2
    WARN = 3
    BRIEF = 4
    INFO = 5
    DEBUG = 6

    def __str__(self) -> str:
        return self.name


class ILogger(abc.ABC):
    @property
    @abc.abstractmethod
    def level(self) -> LogLevel: ...
    @abc.abstractmethod
    def flush(self) -> None: ...
    @abc.abstractmethod
    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None: ...
    @abc.abstractmethod
    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None: ...
    @abc.abstractmethod
    def debug(self, *msg: object) -> None: ...
    @abc.abstractmethod
    def info(self, *msg: object) -> None: ...
    @abc.abstractmethod
    def brief(self, *msg: object) -> None: ...
    @abc.abstractmethod
    def warn(self, *msg: object) -> None: ...
    @abc.abstractmethod
    def error(self, *msg: object) -> None: ...
    @abc.abstractmethod
    def fatal(self, *msg: object) -> None: ...
    @abc.abstractmethod
    def exception(self, e: Exception) -> Exception: ...
    @abc.abstractmethod
    def close(self) -> None: ...


class NullLog(ILogger):
    @property
    def level(self) -> LogLevel:
        return LogLevel.NULL

    def flush(self) -> None:
        pass

    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        pass

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        pass

    def debug(self, *msg: object) -> None:
        pass

    def info(self, *msg: object) -> None:
        pass

    def brief(self, *msg: object) -> None:
        pass

    def warn(self, *msg: object) -> None:
        pass

    def error(self, *msg: object) -> None:
        pass

    def fatal(self, *msg: object) -> None:
        pass

    def exception(self, e: Exception) -> Exception:
        return e

    def close(self) -> None:
        pass
