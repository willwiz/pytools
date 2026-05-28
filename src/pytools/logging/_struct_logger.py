from __future__ import annotations

import traceback
from inspect import getframeinfo, stack
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pytools.parsing import ppfmt

from ._handlers import STDOUT_HANDLER, FileHandler
from ._string_parse import cstr, debug_info, now
from ._trait import BColors, IHandler, ILogger, LogEnum, LogLevel

if TYPE_CHECKING:
    from collections.abc import Sequence


class StructLogger(ILogger):
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
                f"{BColors.UNDERLINE}Logger instance {self!r} created at {now()}{BColors.ENDC}\n"
                f"{'\n'.join(f'  - {hand!r}' for hand in self._handlers.values())}\n"
            )
            h.flush()

    def __del__(self) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"<StrucLogger level={self._level.name}"
            f" header={self._header}"
            f" handlers={len(self._handlers)}>"
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

    def disp(
        self, *msg: object, end: Literal["\n", "\r", ""] = "\n", filt: LogEnum | None = None
    ) -> None:
        if filt and self._level <= filt:
            return
        message = "\n".join([ppfmt(m) for m in msg])
        for h in self._handlers.values():
            h.log(message + end)

    def log(self, *msg: object, level: LogEnum = LogEnum.BRIEF, **kwargs: object) -> None:
        if len(msg) < 1:
            return
        message = "\n".join([ppfmt(m) for m in msg])
        if self._header:
            header = f"[{now()}|{cstr(level)}]>>> "
            message = header + message
        if level > LogEnum.BRIEF:
            tb = getframeinfo(stack()[2][0])
            kwargs = {**debug_info(tb), **kwargs}
            message = message + "\n" + ppfmt(kwargs)
        for h in self._handlers.values():
            h.log(message + "\n")

    def debug(self, *msg: object, **kwargs: object) -> None:
        if self._level <= LogEnum.DEBUG:
            self.log(*msg, level=LogEnum.DEBUG, **kwargs)

    def info(self, *msg: object, **kwargs: object) -> None:
        if self._level <= LogEnum.INFO:
            self.log(*msg, level=LogEnum.INFO, **kwargs)

    def brief(self, *msg: object, **kwargs: object) -> None:
        if self._level <= LogEnum.BRIEF:
            self.log(*msg, level=LogEnum.BRIEF, **kwargs)

    def warn(self, *msg: object, **kwargs: object) -> None:
        if self._level <= LogEnum.WARN:
            self.log(*msg, level=LogEnum.WARN, **kwargs)

    def error(self, *msg: object, **kwargs: object) -> None:
        if self._level <= LogEnum.ERROR:
            self.log(*msg, level=LogEnum.ERROR, **kwargs)

    def fatal(self, *msg: object, **kwargs: object) -> None:
        if self._level <= LogEnum.FATAL:
            self.log(*msg, level=LogEnum.FATAL, **kwargs)

    def exception(self, e: Exception) -> Exception:
        self.disp(traceback.format_exc())
        return e

    def close(self) -> None:
        self._handlers.clear()
