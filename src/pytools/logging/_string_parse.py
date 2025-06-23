from __future__ import annotations

__all__ = [
    "cstr",
    "debug_str",
    "filter_ansi",
    "now",
]
import re
import time
from pathlib import Path
from typing import TYPE_CHECKING

from ._highlight import LB, RB

if TYPE_CHECKING:
    from inspect import Traceback

    from .trait import LogLevel


def now() -> str:
    return time.strftime("%H:%M:%S", time.localtime())


def debug_str(frame: Traceback) -> str:
    file = Path(*Path(frame.filename).parts[-3:])
    return f"({file}:{frame.lineno}|{frame.function})>>>"


def cstr(level: LogLevel) -> str:
    return f"{LB[level]}{level}{RB[level]}"


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


def filter_ansi(text: object) -> str:
    return ANSI_ESCAPE_8BIT.sub("", str(text))


def filter_ansi_char[T: (str, bytes)](text: T) -> T:
    if isinstance(text, str):
        return ANSI_ESCAPE_8BIT.sub("", text)
    if isinstance(text, bytes):
        return ANSI_ESCAPE_8BITB.sub(b"", text)
    err_msg = f"text must be str or bytes, got {type(text).__name__}"
    raise TypeError(err_msg)
