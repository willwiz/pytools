from __future__ import annotations

__all__ = ["LOG_LEVEL", "NULL_LOGGER", "BLogger", "ILogger", "LogLevel", "XLogger"]
import enum
import os
import re
import traceback
from datetime import datetime
from inspect import Traceback, getframeinfo, stack
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TextIO

from .trait import ILogger, LogLevel

if TYPE_CHECKING:
    from collections.abc import Mapping


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")  # noqa: DTZ005


LOG_LEVEL = Literal["NULL", "FATAL", "ERROR", "WARN", "BRIEF", "INFO", "DEBUG"]


class BColors(enum.StrEnum):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


LB: Mapping[LogLevel, str] = {
    LogLevel.NULL: "",
    LogLevel.FATAL: BColors.FAIL,
    LogLevel.ERROR: BColors.FAIL,
    LogLevel.WARN: BColors.WARN,
    LogLevel.BRIEF: BColors.OKCYAN,
    LogLevel.INFO: BColors.OKGREEN,
    LogLevel.DEBUG: BColors.OKBLUE,
}

RB: Mapping[LogLevel, str] = {
    LogLevel.NULL: "",
    LogLevel.FATAL: BColors.ENDC,
    LogLevel.ERROR: BColors.ENDC,
    LogLevel.WARN: BColors.ENDC,
    LogLevel.BRIEF: BColors.ENDC,
    LogLevel.INFO: BColors.ENDC,
    LogLevel.DEBUG: BColors.ENDC,
}


def _debug_str(frame: Traceback) -> str:
    file = Path(*Path(frame.filename).parts[-3:])
    return f"({file}:{frame.lineno}|{frame.function})>>>"


def _cstr(level: LogLevel) -> str:
    return f"{LB[level]}{level}{RB[level]}"


class BLogger(ILogger):
    __slots__ = ["_level"]
    _level: LogLevel

    def __init__(self, level: LOG_LEVEL | LogLevel) -> None:
        self._level = level if isinstance(level, LogLevel) else LogLevel[level]

    @property
    def level(self) -> LogLevel:
        return self._level

    def flush(self) -> None:
        pass

    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        if len(msg) < 1:
            return
        frame = getframeinfo(stack()[2][0])
        print(f"\n[{now()}|{_cstr(level)}]{_debug_str(frame)}", *msg, sep="\n")

    def disp(self, *msg: object, end: Literal["\n", "\r", "\x1b[1K\r", ""] = "\n") -> None:
        if len(msg) < 1:
            return
        print(*msg, sep=end, end=end)

    def debug(self, *msg: object) -> None:
        if self._level >= LogLevel.DEBUG:
            self.print(*msg, level=LogLevel.DEBUG)

    def info(self, *msg: object) -> None:
        if self._level >= LogLevel.INFO:
            self.print(*msg, level=LogLevel.INFO)

    def brief(self, *msg: object) -> None:
        if self._level >= LogLevel.BRIEF:
            self.print(*msg, level=LogLevel.BRIEF)

    def warn(self, *msg: object) -> None:
        if self._level >= LogLevel.WARN:
            self.print(*msg, level=LogLevel.WARN)

    def error(self, *msg: object) -> None:
        if self._level >= LogLevel.ERROR:
            self.print(*msg, level=LogLevel.ERROR)

    def fatal(self, *msg: object) -> None:
        if self._level >= LogLevel.FATAL:
            self.print(*msg, level=LogLevel.FATAL)

    def exception(self, e: Exception) -> Exception:
        print(traceback.format_exc())
        return e


class XLogger(ILogger):
    __slots__ = ["_f", "_level"]
    _level: LogLevel
    _f: TextIO | None
    _h: bool

    def __init__(
        self,
        level: LOG_LEVEL | LogLevel,
        file: str | Path | None = None,
        *,
        debug_str: bool = False,
    ) -> None:
        self._level = level if isinstance(level, LogLevel) else LogLevel[level]
        self._h = debug_str
        if file is None:
            self._f = None
            return
        self._f = open(file, "w")  # noqa: SIM115, PTH123
        self._f.write(
            f"Log file: {file}\nLog file created at {now()}\nLog level: {self._level.name}\n\n",
        )
        self._f.flush()
        os.fsync(self._f.fileno())

    def __del__(self) -> None:
        if self._f is None:
            return
        self._f.write(f"\nLog file closed at {now()}\n")
        self._f.close()

    @property
    def level(self) -> LogLevel:
        return self._level

    def flush(self) -> None:
        if self._f is None:
            return
        self._f.flush()
        os.fsync(self._f.fileno())

    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        if len(msg) < 1:
            return
        frame = getframeinfo(stack()[2][0])
        debug_str = _debug_str(frame)
        message = "\n".join([str(m) for m in msg])
        print(f"\n[{now()}|{_cstr(level)}]{debug_str}", message, sep="\n")
        if self._f is None:
            return
        message = f"\n[{now()}|{_cstr(level)}]{debug_str}" + message if self._h else message
        self._f.write(message + "\n")

    def disp(self, *msg: object, end: Literal["\n", "\r", "\x1b[1K\r", ""] = "\n") -> None:
        if len(msg) < 1:
            return
        message = "\n".join([str(m) for m in msg])
        print(message, end=end)
        if self._f is None:
            return
        self._f.write(message + "\n")

    def debug(self, *msg: object) -> None:
        if self._level >= LogLevel.DEBUG:
            self.print(*msg, level=LogLevel.DEBUG)

    def info(self, *msg: object) -> None:
        if self._level >= LogLevel.INFO:
            self.print(*msg, level=LogLevel.INFO)

    def brief(self, *msg: object) -> None:
        if self._level >= LogLevel.BRIEF:
            self.print(*msg, level=LogLevel.BRIEF)

    def warn(self, *msg: object) -> None:
        if self._level >= LogLevel.WARN:
            self.print(*msg, level=LogLevel.WARN)

    def error(self, *msg: object) -> None:
        if self._level >= LogLevel.ERROR:
            self.print(*msg, level=LogLevel.ERROR)

    def fatal(self, *msg: object) -> None:
        if self._level >= LogLevel.FATAL:
            self.print(*msg, level=LogLevel.FATAL)

    def exception(self, e: Exception) -> Exception:
        print(traceback.format_exc())
        return e


class _NullLogger(ILogger):
    __slots__ = ["_level"]
    _level: LogLevel

    def __init__(self) -> None:
        self._level = LogLevel.NULL

    @property
    def level(self) -> LogLevel:
        return self._level

    def flush(self) -> None:
        pass

    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        pass

    def disp(self, *msg: object, end: Literal["\n", "\r", "\x1b[1K\r", ""] = "\n") -> None:
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


NULL_LOGGER = _NullLogger()
# 7-bit and 8-bit C1 ANSI sequences
ANSI_ESCAPE_8BIT = re.compile(
    r"""
    (?: # either 7-bit C1, two bytes, ESC Fe (omitting CSI)
        \x1B
        [@-Z\\-_]
    |   # or a single 8-bit byte Fe (omitting CSI)
        [\x80-\x9A\x9C-\x9F]
    |   # or CSI + control codes
        (?: # 7-bit CSI, ESC [
            \x1B\[
        |   # 8-bit CSI, 9B
            \x9B
        )
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""",
    re.VERBOSE,
)

# 7-bit and 8-bit C1 ANSI sequences
ANSI_ESCAPE_8BITB = re.compile(
    rb"""
    (?: # either 7-bit C1, two bytes, ESC Fe (omitting CSI)
        \x1B
        [@-Z\\-_]
    |   # or a single 8-bit byte Fe (omitting CSI)
        [\x80-\x9A\x9C-\x9F]
    |   # or CSI + control codes
        (?: # 7-bit CSI, ESC [
        \x1B\[
    |   # 8-bit CSI, 9B
        \x9B
        )
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""",
    re.VERBOSE,
)


def filter_ansi[T: (str, bytes)](text: T) -> T:
    if isinstance(text, str):
        return ANSI_ESCAPE_8BIT.sub("", text)
    if isinstance(text, bytes):
        return ANSI_ESCAPE_8BITB.sub(b"", text)
    err_msg = f"text must be str or bytes, got {type(text).__name__}"
    raise TypeError(err_msg)
