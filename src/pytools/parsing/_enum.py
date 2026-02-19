from __future__ import annotations

import enum
from typing import Generic, TypeVar

__all__ = ["EnumGetter"]

_T_co = TypeVar("_T_co", bound=enum.Enum, covariant=True)


class EnumGetter(Generic[_T_co]):
    __slots__ = ("enum", "upper_case")

    def __init__(self, e: type[_T_co], *, upper_case: bool = False) -> None:
        self.enum = e
        self.upper_case = upper_case

    def __call__(self, value: str) -> _T_co:
        if self.upper_case:
            value = value.upper()
        return self.enum[value]
