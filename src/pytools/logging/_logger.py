from __future__ import annotations

import multiprocessing
import sys
import traceback
from inspect import getframeinfo, stack
from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING, Final, Literal, overload, override

from ._handlers import STDOUT_HANDLER, FileHandler
from ._string_parse import cstr, debug_str, now
from ._trait import BColors, IHandler, ILogger, LogEnum, LogLevel

if TYPE_CHECKING:
    from collections.abc import Sequence


_LOGGERS_DICT: Final[dict[str, ILogger]] = {}
_NOT_NULL = Literal[
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
def get_logger() -> ILogger: ...
@overload
def get_logger(name: str = ..., *, level: Literal["NULL", LogEnum.NULL]) -> _NullLogger: ...
@overload
def get_logger(name: str = ..., *, level: _NOT_NULL) -> BLogger: ...
def get_logger(
    name: str | None = "__main__",
    *,
    level: LogLevel | LogEnum = LogEnum.INFO,
    console: bool = True,
    file: Sequence[str | Path] | None = None,
) -> ILogger:
    if multiprocessing.parent_process() is not None:
        return NLOGGER
    if name is None:
        return NLOGGER
    level = level if isinstance(level, LogEnum) else LogEnum[level]
    logger = _LOGGERS_DICT.get(name)
    if logger is None:
        _LOGGERS_DICT[name] = (
            NLOGGER if level is LogEnum.NULL else BLogger(level=level, stdout=console, files=file)
        )
        return _LOGGERS_DICT[name]
    if logger.level == level:
        return logger
    if logger.level is LogEnum.NULL:
        # Allow NullLogger to be replaced, but not BLoggers
        _LOGGERS_DICT[name] = BLogger(level=level, stdout=console, files=file)
        return _LOGGERS_DICT[name]
    msg = (
        f"Logger '{name}' already exists with level {logger.level.name}. "
        f"Requested level {level.name} is ignored."
    )
    logger.warn(msg)
    return logger


class BLogger(ILogger):
    __slots__ = ["_handlers", "_header", "_level"]
    _level: LogEnum
    _handlers: dict[str, IHandler]
    _header: bool

    def __init__(
        self,
        level: LogLevel | LogEnum,
        *,
        header: bool = True,
        stdout: bool = True,
        files: Sequence[str | Path] | None = None,
    ) -> None:
        self._level = level if isinstance(level, LogEnum) else LogEnum[level]
        self._header = header
        self._handlers = {"STDOUT": STDOUT_HANDLER} if stdout else {}
        if files is not None:
            self._handlers.update({str(f): FileHandler(f) for f in files})
        for h in self._handlers.values():
            if self._level < LogEnum.BRIEF:
                continue
            h.log(
                f"Logger instance: {self!r} created at {now()}\n"
                f"{BColors.UNDERLINE}Logger created with level: "
                f"{self._level.name}{BColors.ENDC}\n\n"
            )
            h.flush()

    def __del__(self) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"<BLogger level={self._level.name} header={self._header} >\n"
            f"handlers={len(self._handlers)}>\n" + pformat(self._handlers)
        )

    @property
    def header(self) -> bool:
        return self._header

    @property
    def level(self) -> LogEnum:
        return self._level

    @level.setter
    def level(self, level: LogLevel | LogEnum) -> None:
        self._level = level if isinstance(level, LogEnum) else LogEnum[level]

    @property
    def console(self) -> bool:
        return "STDOUT" in self._handlers

    @console.setter
    def console(self, console: bool) -> None:
        if ("STDOUT" in self._handlers) == console:
            return
        if console:
            self._handlers["STDOUT"] = STDOUT_HANDLER
            return
        del self._handlers["STDOUT"]

    def add_handler(self, handler: IHandler | Path | str, *, name: str | None = None) -> None:
        if isinstance(handler, (str, Path)):
            handler = FileHandler(handler)
        key = name or repr(handler)
        self._handlers[key] = handler

    def remove_handler(self, handler: IHandler | str) -> None:
        key = handler if isinstance(handler, str) else repr(handler)
        if key in self._handlers:
            del self._handlers[key]

    def flush(self) -> None:
        for h in self._handlers.values():
            h.flush()

    def log(self, *msg: object, level: LogEnum = LogEnum.BRIEF) -> None:
        if len(msg) < 1:
            return
        if self._header:
            tb = getframeinfo(stack()[2][0])
            header = f"\n[{now()}|{cstr(level)}]{debug_str(tb)}\n"
            for h in self._handlers.values():
                h.log(header)
        self.disp(*msg)

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        message = "\n".join([str(m) for m in msg])
        for h in self._handlers.values():
            h.log(message + end)

    def debug(self, *msg: object) -> None:
        if self._level >= LogEnum.DEBUG:
            self.log(*msg, level=LogEnum.DEBUG)

    def info(self, *msg: object) -> None:
        if self._level >= LogEnum.INFO:
            self.log(*msg, level=LogEnum.INFO)

    def brief(self, *msg: object) -> None:
        if self._level >= LogEnum.BRIEF:
            self.log(*msg, level=LogEnum.BRIEF)

    def warn(self, *msg: object) -> None:
        if self._level >= LogEnum.WARN:
            self.log(*msg, level=LogEnum.WARN)

    def error(self, *msg: object) -> None:
        if self._level >= LogEnum.ERROR:
            self.log(*msg, level=LogEnum.ERROR)

    def fatal(self, *msg: object) -> None:
        if self._level >= LogEnum.FATAL:
            self.log(*msg, level=LogEnum.FATAL)

    def exception(self, e: Exception) -> Exception:
        self.disp(traceback.format_exc())
        return e

    def close(self) -> None:
        self._handlers.clear()


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

    def add_handler(self, handler: IHandler | Path | str, *, name: str | None = None) -> None:
        pass

    def remove_handler(self, handler: IHandler | str) -> None:
        pass

    def flush(self) -> None:
        pass

    def log(self, *msg: object, level: LogEnum = LogEnum.BRIEF) -> None:
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
        sys.stderr.write("<<< Warning: " + "\n".join(str(m) for m in msg) + "\n")

    def error(self, *msg: object) -> None:
        sys.stderr.write("<<< Error: " + "\n".join(str(m) for m in msg) + "\n")

    def fatal(self, *msg: object) -> None:
        sys.stderr.write("<<< Fatal: " + "\n".join(str(m) for m in msg) + "\n")

    def exception(self, e: Exception) -> Exception:
        return e

    def close(self) -> None:
        pass


NLOGGER: ILogger = _NullLogger()
