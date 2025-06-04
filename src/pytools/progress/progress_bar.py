from typing import Final, Literal, TypedDict, Unpack


class PBarKwargs(TypedDict, total=False):
    """Keyword arguments for the ProgressBar class."""

    length: int
    decimal: int
    pixel: str
    end: Literal["\n", "\r", ""]


class ProgressBar:
    __slots__ = ["_b", "_bmt", "_endl", "_l", "_n", "_p", "_pmt", "_s", "i"]

    _n: Final[int]
    i: int
    _l: Final[int]
    _p: Final[str]
    _s: Final[str]
    _b: Final[str]
    _endl: Final[Literal["\n", "\r", ""]]
    _bmt: Final[str]
    _pmt: Final[str]

    def __init__(
        self,
        bound: int,
        prefix: str = "",
        suffix: str = "",
        **kwargs: Unpack[PBarKwargs],
        # length: int = 50,
        # decimal: int = 1,
        # pixel: str = "*",
        # end: Literal["\n", "\r", ""] = "",
    ) -> None:
        self.i, self._n = 0, bound
        self._p, self._s = prefix, suffix
        self._b = kwargs.get("pixel", "*")
        self._l = kwargs.get("length", 50) * len(self._b)
        self._bmt = f"-<{self._l}"
        decimal = kwargs.get("decimal", 1)
        self._pmt = f">{5 + decimal}.{decimal}%"
        self._endl = kwargs.get("end", "\r")

    def reset(self) -> None:
        self.i = 0

    def next(self) -> None:
        self.i = self.i + 1
        self._print_bar(self.i)

    def finish(self) -> None:
        self._print_bar(self._n)

    def _print_bar(self, i: int) -> None:
        p = 1.0 if (self._n == 0) else (i / self._n)
        f = self._b * int(self._l * p)
        bar = f"\r{self._p}|{f:{self._bmt}}|{p:{self._pmt}}{self._s}"
        print(bar, end=self._endl)
        if i == self._n:
            print()
