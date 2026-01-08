import traceback
from collections.abc import Sequence
from inspect import getframeinfo, stack
from pathlib import Path
from pprint import pformat
from typing import Literal

from ._handlers import STDOUT_HANDLER, FileHandler
from ._string_parse import cstr, debug_str, now
from .trait import LOG_LEVEL, BColors, IHandler, ILogger, LogLevel


class BLogger(ILogger):
    __slots__ = ["_handlers", "_header", "_level"]
    _level: LogLevel
    _handlers: list[IHandler]
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
        self._handlers = [STDOUT_HANDLER] if stdout else []
        if files is not None:
            self._handlers += [FileHandler(Path(f)) for f in files]
        for h in self._handlers:
            h.log(
                f"{BColors.UNDERLINE}Log file created at {now()}\n"
                f"Log level: {self._level.name}{BColors.ENDC}\n\n",
            )
            h.flush()

    def __del__(self) -> None:
        self.close()

    @property
    def header(self) -> bool:
        return self._header

    @property
    def level(self) -> LogLevel:
        return self._level

    def flush(self) -> None:
        for h in self._handlers:
            h.flush()

    def log(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        if len(msg) < 1:
            return
        if self._header:
            tb = getframeinfo(stack()[2][0])
            header = f"\n[{now()}|{cstr(level)}]{debug_str(tb)}\n"
            for h in self._handlers:
                h.log(header)
        self.disp(*msg)

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        message = "\n".join([pformat(m, compact=True, sort_dicts=False) for m in msg])
        for h in self._handlers:
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
        for h in self._handlers:
            h.log(f"\n\n{BColors.UNDERLINE}Log file closed at {now()}{BColors.ENDC}\n")
        self._handlers.clear()
