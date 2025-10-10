from __future__ import annotations

__all__ = ["NLOGGER", "BLogger", "TLogger", "TXLogger", "XLogger"]
import os
import sys
import traceback
from concurrent.futures import Executor, ThreadPoolExecutor
from inspect import Traceback, getframeinfo, stack
from multiprocessing import Lock
from typing import TYPE_CHECKING, Literal, TextIO

from ._string_parse import cstr, debug_str, filter_ansi, now
from .trait import LOG_LEVEL, ILogger, LogLevel

if TYPE_CHECKING:
    from multiprocessing.synchronize import Lock as LockBase
    from pathlib import Path


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
        print(f"\n[{now()}|{cstr(level)}]{debug_str(frame)}", *msg, sep="\n")

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
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
        self.disp(traceback.format_exc())
        return e

    def close(self) -> None:
        pass  # No resources to close for BLogger


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
        if self._f.closed:
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
        header = f"\n[{now()}|{cstr(level)}]{debug_str(frame)}"
        message = "\n".join([str(m) for m in msg])
        print(header, message)
        if self._f is None:
            return
        message = f"{header}\n{message}" if self._h else message
        self._f.write(filter_ansi(message).replace("\r", "") + "\n")

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        if len(msg) < 1:
            return
        message = "\n".join([str(m) for m in msg])
        print(message, end=end)
        if self._f is None:
            return
        self._f.write(filter_ansi(message).replace("\r", "") + "\n")

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
        self.disp(traceback.format_exc())
        return e

    def close(self) -> None:
        if self._f is None:
            return
        if self._f.closed:
            return
        self._f.write(f"\nLog file closed at {now()}\n")
        self._f.close()


class TLogger(ILogger):
    __slots__ = ["_level", "_lock", "_thread"]
    _lock: LockBase
    _level: LogLevel
    _thread: Executor

    def __init__(self, level: LOG_LEVEL | LogLevel) -> None:
        self._level = level if isinstance(level, LogLevel) else LogLevel[level]
        self._lock = Lock()
        self._thread = ThreadPoolExecutor(max_workers=1)

    def __del__(self) -> None:
        self._thread.shutdown(wait=True)

    @property
    def level(self) -> LogLevel:
        return self._level

    def flush(self) -> None:
        pass

    def _async_print(
        self,
        frame: Traceback,
        lock: LockBase,
        *msg: object,
        level: LogLevel = LogLevel.BRIEF,
    ) -> None:
        with lock:
            print(f"\n[{now()}|{cstr(level)}]{debug_str(frame)}", *msg, sep="\n")

    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        if len(msg) < 1:
            return
        frame = getframeinfo(stack()[2][0])
        self._thread.submit(self._async_print, frame, self._lock, *msg, level=level)

    def _async_disp(
        self,
        lock: LockBase,
        *msg: object,
        end: Literal["\n", "\r", ""] = "\n",
    ) -> None:
        with lock:
            message = end.join([str(m) for m in msg])
            sys.stdout.write(message + end)

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        if len(msg) < 1:
            return
        self._thread.submit(self._async_disp, self._lock, *msg, end=end)

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
        self.disp(traceback.format_exc())
        return e

    def close(self) -> None:
        self._thread.shutdown(wait=True)


class TXLogger(ILogger):
    """Threaded logger that writes to a file."""

    __slots__ = ["_f", "_h", "_level", "_lock", "_thread"]
    _level: LogLevel
    _thread: Executor
    _f: TextIO | None
    _h: bool
    _lock: LockBase

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
        self._thread = ThreadPoolExecutor(max_workers=1)
        self._lock = Lock()
        self._f = open(file, "w")  # noqa: SIM115, PTH123
        self._f.write(
            f"Log file: {file}\nLog file created at {now()}\nLog level: {self._level.name}\n\n",
        )
        self._f.flush()
        os.fsync(self._f.fileno())

    def __del__(self) -> None:
        self._thread.shutdown(wait=True)
        if self._f is None:
            return
        if self._f.closed:
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

    def _print_async(
        self,
        frame: Traceback,
        lock: LockBase,
        *msg: object,
        level: LogLevel = LogLevel.BRIEF,
    ) -> None:
        with lock:
            header = f"\n[{now()}|{cstr(level)}]{debug_str(frame)}"
            message = "\n".join([str(m) for m in msg])
            sys.stdout.write(f"{header}\n{message}" + "\n")
            if self._f is None:
                return
            message = f"{header}\n{message}" if self._h else message
            self._f.write(filter_ansi(message).replace("\r", "") + "\n")

    def print(self, *msg: object, level: LogLevel = LogLevel.BRIEF) -> None:
        if len(msg) < 1:
            return
        frame = getframeinfo(stack()[2][0])
        self._thread.submit(self._print_async, frame, self._lock, *msg, level=level)

    def _disp_async(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        with self._lock:
            message = "\n".join([str(m) for m in msg])
            sys.stdout.write(message + end)
            if self._f is None:
                return
            self._f.write(filter_ansi(message).replace("\r", "") + "\n")

    def disp(self, *msg: object, end: Literal["\n", "\r", ""] = "\n") -> None:
        if len(msg) < 1:
            return
        self._thread.submit(self._disp_async, *msg, end=end)

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
        self.disp(traceback.format_exc())
        return e

    def close(self) -> None:
        self._thread.shutdown(wait=True)
        if self._f is None:
            return
        if self._f.closed:
            return
        self._f.write(f"\nLog file closed at {now()}\n")
        self._f.close()


class _NullLogger(ILogger):
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


NLOGGER: ILogger = _NullLogger()
