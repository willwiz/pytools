from __future__ import annotations

from typing import Final, Literal, TypedDict, Unpack

from pytools.logging import ILogger, get_logger

__all__ = ["ProgressBar"]


class PBarKwargs(TypedDict, total=False):
    """Keyword arguments for the ProgressBar class."""

    length: int
    decimal: int
    pixel: str
    end: Literal["\n", "\r", ""]


class ProgressBar:
    __slots__ = [
        "_bdiv",
        "_bmt",
        "_dec",
        "_endl",
        "_l",
        "_log",
        "_n",
        "_pdiv",
        "_pfx",
        "_pmt",
        "_sfx",
        "_x",
        "b",
        "bar",
        "i",
        "p",
    ]

    _x: Final[str]
    _n: Final[int]
    _l: Final[int]
    _pfx: Final[str]
    _sfx: Final[str]
    _endl: Final[Literal["\n", "\r", ""]]
    _bmt: Final[str]
    _pmt: Final[str]
    _bdiv: Final[float]
    _pdiv: Final[float]
    _dec: Final[float]
    _log: Final[ILogger]
    b: int
    i: int
    p: float
    bar: str

    def __init__(
        self,
        n: int,
        prefix: str = "",
        suffix: str = "",
        **kwargs: Unpack[PBarKwargs],
    ) -> None:
        self.i, self.b, self.p, self._n = 0, 0, 0, n
        self._pfx, self._sfx = prefix, suffix
        self._x = kwargs.get("pixel", "*")
        decimal = kwargs.get("decimal", 1)
        length = kwargs.get("length", 50)
        self._l = length * len(self._x)
        self._pdiv = 1.0 / n
        self._bdiv = length / n
        self._bmt = f"-<{self._l}"
        self._pmt = f">{5 + decimal}.{decimal}%"
        self._endl = kwargs.get("end", "\r")
        self.bar = f"{self._pfx}|{' ':{self._bmt}}|"
        self._dec = 0.01 * 0.1**decimal
        self._log = get_logger()

    def reset(self) -> None:
        self.i = 0
        self.p = 0
        self.b = 0
        self.bar = f"{self._pfx}|{' ':{self._bmt}}|"

    def next(self) -> None:
        self.i = self.i + 1
        self._print_bar()

    def finish(self) -> None:
        self._print_bar()

    def _print_bar(self) -> None:
        p = self._pdiv * self.i
        if (p - self.p) < self._dec:
            return
        self.p = p
        b = int(self._bdiv * self.i)
        if self.b != b:
            self.b = b
            self.bar = f"{self._pfx}|{self._x * b:{self._bmt}}|"
        self._log.disp(self._endl)
        self._log.disp(self.bar)
        self._log.disp(f"{p:{self._pmt}}{self._sfx}")
        if self.i >= self._n:
            self._log.disp("\n")
        self._log.flush()
