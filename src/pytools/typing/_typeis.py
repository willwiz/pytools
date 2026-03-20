from collections.abc import Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    TypeAliasType,
    TypeIs,
    get_args,
)

if TYPE_CHECKING:
    from types import UnionType

__all__ = ["is_sequence", "is_sequence_t", "is_type"]


def is_sequence(args: object) -> TypeIs[Sequence[Any]]:
    return isinstance(args, Sequence)


def is_type[T: Any](args: object, kind: type[T] | UnionType | TypeAliasType) -> TypeIs[T]:
    if isinstance(kind, TypeAliasType):
        return is_type(args, kind.__value__)
    origins = get_args(kind)
    if len(origins) > 1:
        return args in get_args(kind)
    return isinstance(args, kind)


def is_sequence_t[T: Any](
    args: object, kind: type[T] | UnionType | TypeAliasType
) -> TypeIs[Sequence[T]]:
    if not is_sequence(args):
        return False
    return all(is_type(i, kind) for i in args)
