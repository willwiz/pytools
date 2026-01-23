from __future__ import annotations

import re
import time
from pathlib import Path
from typing import TYPE_CHECKING, Final

from pytools.result import Err, Ok

from ._trait import BColors, LogLevel

if TYPE_CHECKING:
    from inspect import Traceback

__all__ = ["cstr", "debug_str", "filter_ansi", "now"]

LB: Final = {
    LogLevel.NULL: BColors.NULL,
    LogLevel.FATAL: BColors.FAIL,
    LogLevel.ERROR: BColors.FAIL,
    LogLevel.WARN: BColors.WARN,
    LogLevel.BRIEF: BColors.OKCYAN,
    LogLevel.INFO: BColors.OKGREEN,
    LogLevel.DEBUG: BColors.OKBLUE,
}

RB: Final = {
    LogLevel.NULL: BColors.ENDC,
    LogLevel.FATAL: BColors.ENDC,
    LogLevel.ERROR: BColors.ENDC,
    LogLevel.WARN: BColors.ENDC,
    LogLevel.BRIEF: BColors.ENDC,
    LogLevel.INFO: BColors.ENDC,
    LogLevel.DEBUG: BColors.ENDC,
}


def now() -> str:
    return time.strftime("%H:%M:%S", time.localtime())


def debug_str(tb: Traceback) -> str:
    file = Path(*Path(tb.filename).parts[-3:])
    return f"({file}:{tb.lineno}|{tb.function})>>>"


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


def filter_ansi_char[T: (str, bytes)](text: T) -> Ok[T] | Err:
    if isinstance(text, str):
        return Ok(ANSI_ESCAPE_8BIT.sub("", text))
    if isinstance(text, bytes):
        return Ok(ANSI_ESCAPE_8BITB.sub(b"", text))
    err_msg = f"text must be str or bytes, got {type(text).__name__}"
    return Err(TypeError(err_msg))
