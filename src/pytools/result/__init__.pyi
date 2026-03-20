# ruff: noqa: D418, PYI021
from collections.abc import Mapping, Sequence
from typing import Any, Generic, Never, TypeGuard, TypeVar, overload

_T_co = TypeVar("_T_co", covariant=True)

class Err:
    __slots__ = ("val",)
    __match_args__ = ("val",)
    val: Exception

    def __init__(self, value: Exception) -> None: ...
    def unwrap(self) -> Never: ...
    def unwrap_or[O: Any](self, default: O, /) -> O: ...
    def next(self) -> Err: ...
    def ok(self) -> bool: ...

class Ok(Generic[_T_co]):  # noqa: UP046
    __slots__ = ("val",)
    __match_args__ = ("val",)
    val: _T_co

    def __init__(self, value: _T_co) -> None: ...
    def unwrap(self) -> _T_co: ...
    def unwrap_or[O: Any](self, _default: O, /) -> _T_co | O: ...
    def next(self) -> Ok[_T_co]: ...
    def ok(self) -> bool: ...

type Result[T] = Ok[T] | Err

@overload
def all_ok[T](
    result: Sequence[Ok[T] | Err],
) -> Ok[Sequence[T]] | Err:
    """Return Ok[Sequence[T]] if all results are Ok, otherwise return the first Err.

    Parameters
    ----------
    result : Sequence[Ok[T] | Err]
    A sequence of Ok or Err results.

    Returns
    -------
    Ok[Sequence[T]] | Err
    An Ok containing a sequence of T if all results are Ok, otherwise an Err.

    """

@overload
def all_ok[K, V](
    result: Mapping[K, Ok[V] | Err],
) -> Ok[Mapping[K, V]] | Err:
    """Return Ok[Mapping[K, V]] if all results are Ok, otherwise return the first Err.

    Parameters
    ----------
    result : Mapping[K, Ok[V] | Err]
        A mapping of Ok or Err results.

    Returns
    -------
    Ok[Mapping[K, V]] | Err
        An Ok containing a mapping of V if all results are Ok, otherwise an Err.

    """

@overload
def filter_ok[V](results: Sequence[Ok[V] | Err]) -> Sequence[V]: ...
@overload
def filter_ok[K, V](results: Mapping[K, Ok[V] | Err]) -> Mapping[K, V]: ...
@overload
def is_all_ok[T](results: Sequence[Ok[T] | Err]) -> TypeGuard[Sequence[Ok[T]]]: ...
@overload
def is_all_ok[K, V](results: Mapping[K, Ok[V] | Err]) -> TypeGuard[Mapping[K, Ok[V]]]: ...
