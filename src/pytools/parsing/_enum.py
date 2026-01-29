from __future__ import annotations

import enum

__all__ = ["EnumGetter"]


class EnumGetter[T: enum.Enum]:
    __slots__ = ("enum", "upper_case")

    def __init__(self, e: type[T], *, upper_case: bool = False) -> None:
        self.enum = e
        self.upper_case = upper_case

    def __call__(self, value: str) -> T:
        if self.upper_case:
            value = value.upper()
        return self.enum[value]
