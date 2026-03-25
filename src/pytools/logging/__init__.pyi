from collections.abc import Sequence
from pathlib import Path
from typing import Literal, overload

from ._trait import BColors as BColors
from ._trait import IHandler as IHandler
from ._trait import ILogger as ILogger
from ._trait import LogEnum as LogEnum
from ._trait import LogLevel as LogLevel

NLOGGER: ILogger

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
