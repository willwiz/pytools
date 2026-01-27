from __future__ import annotations

import sys
import traceback
from inspect import getframeinfo, stack
from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING, Final, Literal

from ._handlers import STDOUT_HANDLER, FileHandler
from ._string_parse import cstr, debug_str, now
from ._trait import LOG_LEVEL, BColors, IHandler, ILogger, LogLevel

if TYPE_CHECKING:
    from collections.abc import Sequence


_LOGGERS_DICT: Final[dict[str, ILogger]] = {}


def get_logger(name: str = "__root__", level: LOG_LEVEL | LogLevel = LogLevel.NULL) -> ILogger:
    level = level if isinstance(level, LogLevel) else LogLevel[level]
    if name in _LOGGERS_DICT:
        logger = _LOGGERS_DICT[name]
        if logger.level != level:
            msg = f"Logger '{name}' level does not match the requested level. Skipped"
            logger.warn(msg)
        return logger
    if level is LogLevel.NULL:
        return NLOGGER
    _LOGGERS_DICT[name] = BLogger(level=level)
    return _LOGGERS_DICT[name]


class BLogger(ILogger):
    __slots__ = ["_handlers", "_header", "_level"]
    _level: LogLevel
    _handlers: dict[str, IHandler]
    _header: bool

    def __init__(
        self,
        level: LOG_LEVEL | LogLevel,
        *,
        header: bool = True,
        stdout: bool = True,
        files: Sequence[str | Path] | None = None,
    ) -> None:
        self._level = level if isinstance(level, LogLevel) else LogLevel[level]
        self._header = header
        self._handlers = {"stdout": STDOUT_HANDLER} if stdout else {}
        if files is not None:
            self._handlers.update({repr(f): FileHandler(f) for f in files})
        for h in self._handlers.values():
            if self._level < LogLevel.INFO:
                continue
            h.log(
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
    def level(self) -> LogLevel:
        return self._level

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

    def log(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
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
        if self._level >= LogLevel.DEBUG:
            self.log(*msg, level=LogLevel.DEBUG)

    def info(self, *msg: object) -> None:
        if self._level >= LogLevel.INFO:
            self.log(*msg, level=LogLevel.INFO)

    def brief(self, *msg: object) -> None:
        if self._level >= LogLevel.BRIEF:
            self.log(*msg, level=LogLevel.BRIEF)

    def warn(self, *msg: object) -> None:
        if self._level >= LogLevel.WARN:
            self.log(*msg, level=LogLevel.WARN)

    def error(self, *msg: object) -> None:
        if self._level >= LogLevel.ERROR:
            self.log(*msg, level=LogLevel.ERROR)

    def fatal(self, *msg: object) -> None:
        if self._level >= LogLevel.FATAL:
            self.log(*msg, level=LogLevel.FATAL)

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
    def level(self) -> LogLevel:
        return LogLevel.NULL

    def add_handler(self, handler: IHandler | Path | str, *, name: str | None = None) -> None:
        pass

    def remove_handler(self, handler: IHandler | str) -> None:
        pass

    def flush(self) -> None:
        pass

    def log(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
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
