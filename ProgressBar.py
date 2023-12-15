#!/usr/bin/env python3
__all__ = ["progress_bar"]

from typing import Final


_FULL_BAR: Final[str] = 50 * "*"


class progress_bar:
    __slots__ = ("n", "msg", "t", "i")

    n: Final[int]
    msg: Final[str]
    t: Final[float]
    i: int

    def _print_bar(self):
        if self.i == self.n:
            print(f"\r{self.msg} |{_FULL_BAR}| 100.0%%", end="\r\n")
        else:
            percent = self.i * self.t
            filledLength = int(percent // 2)
            bar = filledLength * "*" + (50 - filledLength) * "-"
            print(f"\r{self.msg} |{bar}| {percent:.1f}%%", end="\r")

    def __init__(self, message: str, max=100):
        self.n = max
        self.t = 100.0 / max
        self.msg = message
        self.i = 0
        self._print_bar()

    def next(self):
        self.i = self.i + 1
        self._print_bar()

    def finish(self):
        self._print_bar()
