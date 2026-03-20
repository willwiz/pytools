from collections.abc import Sequence
from types import UnionType
from typing import Any, TypeAliasType, TypeIs

__all__ = ["is_sequence", "is_sequence_t", "is_type"]

def is_sequence(args: object) -> TypeIs[Sequence[Any]]: ...
def is_type[T: Any](args: object, kind: type[T] | UnionType | TypeAliasType) -> TypeIs[T]: ...
def is_sequence_t[T: Any](
    args: object, kind: type[T] | UnionType | TypeAliasType
) -> TypeIs[Sequence[T]]: ...
