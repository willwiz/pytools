from __future__ import annotations

import multiprocessing
import sys
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, override

from ._basic_logger import BLogger
from ._struct_logger import StructLogger
from ._trait import IHandler, ILogger, LogEnum, LogLevel

if TYPE_CHECKING:
    from collections.abc import Sequence


if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


_LOGGERS_DICT: Final[dict[str, ILogger]] = {}


def _create_logger(
    level: LogLevel | LogEnum,
    file: Sequence[str | Path] | None = None,
    *,
    console: bool = True,
    logger: Literal["struct", "basic"] = "struct",
) -> ILogger:
    match logger:
        case "struct":
            return StructLogger(level=level, stdout=console, files=file)
        case "basic":
            return BLogger(level=level, stdout=console, files=file)


def get_logger(
    name: str | None = "__main__",
    *,
    level: LogLevel | LogEnum | None = None,
    console: bool = True,
    file: Sequence[str | Path] | None = None,
    logger: Literal["struct", "basic"] = "struct",
) -> ILogger:
    if (
        multiprocessing.parent_process() is not None
        or threading.current_thread() is not threading.main_thread()
    ) or (name is None):
        return NLOGGER
    log = _LOGGERS_DICT.get(name)
    if log is None:
        level = LogEnum.INFO if level is None else level
        level = level if isinstance(level, LogEnum) else LogEnum[level]
        _LOGGERS_DICT[name] = (
            NLOGGER
            if level is LogEnum.NULL
            else _create_logger(level=level, console=console, file=file, logger=logger)
        )
        return _LOGGERS_DICT[name]
    if level is None or (log.level == level):
        return log
    if log.level is LogEnum.NULL:
        # Allow NullLogger to be replaced, but not BLoggers
        _LOGGERS_DICT[name] = _create_logger(level=level, console=console, file=file, logger=logger)
        return _LOGGERS_DICT[name]
    msg = (
        f"Logger '{name}' already exists with level {log.level!s}. "
        f"Requested level {level!s} is ignored."
    )
    log.debug(msg)
    return log


class _NullLogger(ILogger):
    def __repr__(self) -> str:
        return "<NullLogger>"

    @property
    def header(self) -> bool:
        return False

    @property
    def level(self) -> LogEnum:
        return LogEnum.NULL

    @level.setter
    @override
    def level(self, level: LogLevel | LogEnum) -> None:
        sys.stderr.write("<<< Warning: Cannot set level on NullLogger\n")

    @property
    def console(self) -> bool:
        return True

    @console.setter
    @override
    def console(self, console: bool) -> None:
        sys.stderr.write("<<< Warning: Cannot set console on NullLogger\n")

    def add_handler(self, handler: IHandler | Path | str, *, name: str | None = None) -> None: ...

    def remove_handler(self, handler: IHandler | str) -> None: ...

    def flush(self) -> None: ...

    @override
    def log(self, *msg: object, level: LogEnum = LogEnum.BRIEF, **kwargs: object) -> None: ...

    @override
    def disp(
        self, *msg: object, end: Literal["\n", "\r", ""] = "\n", filt: LogEnum | None = None
    ) -> None: ...

    @override
    def debug(self, *msg: object, **kwargs: object) -> None: ...

    @override
    def info(self, *msg: object, **kwargs: object) -> None: ...
    @override
    def brief(self, *msg: object, **kwargs: object) -> None: ...
    @override
    def warn(self, *msg: object, **kwargs: object) -> None:
        sys.stderr.write("<<< Warning: " + "\n".join(str(m) for m in msg) + "\n")

    @override
    def error(self, *msg: object, **kwargs: object) -> None:
        sys.stderr.write("<<< Error: " + "\n".join(str(m) for m in msg) + "\n")

    @override
    def fatal(self, *msg: object, **kwargs: object) -> None:
        sys.stderr.write("<<< Fatal: " + "\n".join(str(m) for m in msg) + "\n")

    def exception(self, e: Exception) -> Exception:
        return e

    def close(self) -> None: ...


NLOGGER: ILogger = _NullLogger()
