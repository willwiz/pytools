import abc
import enum
from collections.abc import Sequence
from pathlib import Path
from typing import Literal, overload

NLOGGER: ILogger
type LogLevel = Literal["NULL", "FATAL", "ERROR", "WARN", "BRIEF", "INFO", "DEBUG"]

class LogEnum(enum.IntEnum):
    NULL = 0
    FATAL = 1
    ERROR = 2
    WARN = 3
    BRIEF = 4
    INFO = 5
    DEBUG = 6

class BColors(enum.StrEnum):
    NULL = ""
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

type _NOT_NULL = Literal[
    "DEBUG",
    "INFO",
    "BRIEF",
    "WARN",
    "ERROR",
    "FATAL",
    LogEnum.DEBUG,
    LogEnum.INFO,
    LogEnum.BRIEF,
    LogEnum.WARN,
    LogEnum.ERROR,
    LogEnum.FATAL,
]

class IHandler(abc.ABC):
    @abc.abstractmethod
    def __del__(self) -> None: ...
    @abc.abstractmethod
    def log(self, msg: str) -> None: ...
    @abc.abstractmethod
    def flush(self) -> None: ...

class ILogger(abc.ABC):
    @property
    @abc.abstractmethod
    def header(self) -> bool: ...
    @property
    @abc.abstractmethod
    def level(self) -> LogEnum: ...
    @property
    @abc.abstractmethod
    def console(self) -> bool: ...
    @abc.abstractmethod
    def add_handler(self, handler: IHandler | str | Path, *, name: str | None = None) -> None: ...
    @abc.abstractmethod
    def remove_handler(self, handler: IHandler | str) -> None: ...
    @abc.abstractmethod
    def flush(self) -> None: ...
    @abc.abstractmethod
    def log(self, *msg: object, level: LogEnum = ...) -> None: ...
    @abc.abstractmethod
    def disp(
        self, *msg: object, end: Literal["\n", "\r", ""] = ..., filt: LogEnum | None = ...
    ) -> None: ...
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

@overload
def get_logger(name: None) -> ILogger: ...
@overload
def get_logger(
    *, console: bool = ..., file: Sequence[str | Path] | None = ..., verbose: bool = ...
) -> ILogger: ...
@overload
def get_logger(
    name: str = ...,
    *,
    level: Literal["NULL", LogEnum.NULL],
    console: bool = ...,
    file: Sequence[str | Path] | None = ...,
    verbose: bool = ...,
) -> ILogger: ...
@overload
def get_logger(
    name: str = ...,
    *,
    level: _NOT_NULL | None,
    console: bool = ...,
    file: Sequence[str | Path] | None = ...,
    verbose: bool = ...,
) -> ILogger: ...
