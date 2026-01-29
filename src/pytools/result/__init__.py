from __future__ import annotations

# ruff: noqa: D418
import abc
import inspect
import types
from collections.abc import Mapping, Sequence
from typing import Any, Never, TypeGuard, cast, overload

__all__ = ["Err", "Ok", "all_ok", "filter_ok"]


class _ResultType[T: Any](abc.ABC):
    @abc.abstractmethod
    def unwrap(self) -> T:
        pass

    @abc.abstractmethod
    def unwrap_or[O: Any](self, default: O, /) -> T | O:
        pass

    @abc.abstractmethod
    def next(self) -> _ResultType[T]:
        pass


class Ok[T: Any](_ResultType[T]):
    __slots__ = ("val",)
    __match_args__ = ("val",)
    val: T

    def __init__(self, value: T) -> None:
        self.val = value

    def unwrap(self) -> T:
        return self.val

    def unwrap_or[O: Any](self, _default: O, /) -> T:  # type: ignore[reportInvalidTypeVarUse]
        return self.val

    def next(self) -> Ok[T]:
        return self


class Err(_ResultType[Never]):
    __slots__ = ("val",)
    __match_args__ = ("val",)
    val: Exception

    def __init__(self, value: Exception) -> None:
        match inspect.currentframe():
            case types.FrameType(f_back=frame):
                if frame is None:
                    msg = "Failed to get caller frame for Err."
                    raise RuntimeError(msg)
                tb = types.TracebackType(value.__traceback__, frame, frame.f_lasti, frame.f_lineno)
            case None:
                msg = "Failed to get current frame for Err. Should never reach here."
                raise RuntimeError(msg)
        self.val = value.with_traceback(tb)

    def unwrap(self) -> Never:
        raise self.val

    def unwrap_or[O: Any](self, default: O, /) -> O:
        return default

    def next(self) -> Err:
        return Err(self.val)


def is_ok_sequence[T](results: Sequence[Ok[T] | Err]) -> TypeGuard[Sequence[Ok[T]]]:
    """Is a sequence of results all Ok[T]."""
    return all(isinstance(res, Ok) for res in results)


def _all_ok_dict[K, V](result: Mapping[K, Ok[V] | Err]) -> Ok[Mapping[K, V]] | Err:
    """Return Ok[dict[Any, T]] if all results are Ok, otherwise return the first Err.

    Parameters
    ----------
    result : Mapping[Any, Ok[T] | Err]
        A mapping of Ok or Err results.

    Returns
    -------
    Ok[Mapping[Any, T]] | Err
        An Ok containing a mapping of T if all results are Ok, otherwise an Err.

    """
    for res in result.values():
        if isinstance(res, Err):
            return Err(res.val)
    return Ok({key: res.val for key, res in cast("Mapping[K, Ok[V]]", result).items()})


def _all_ok_sequence[V](result: Sequence[Ok[V] | Err]) -> Ok[Sequence[V]] | Err:
    """Return Ok[Sequence[V]] if all results are Ok, otherwise return the first Err.

    Parameters
    ----------
    result : Sequence[Ok[V] | Err]
        A sequence of Ok or Err results.

    Returns
    -------
    Ok[Sequence[V]] | Err
        An Ok containing a sequence of V if all results are Ok, otherwise an Err.

    """
    for res in result:
        if isinstance(res, Err):
            return Err(res.val)
    return Ok([res.val for res in cast("Sequence[Ok[V]]", result)])


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


def all_ok[K, V](
    result: Sequence[Ok[V] | Err] | Mapping[K, Ok[V] | Err],
):
    match result:
        case Mapping():
            return _all_ok_dict(result)
        case Sequence():
            return _all_ok_sequence(result)


def filter_ok[T](results: Sequence[Ok[T] | Err]) -> Sequence[T]:
    """Filter out all Ok values from a sequence of Ok and Err results.

    Parameters
    ----------
    results : Sequence[Ok[T] | Err]
        A sequence of Ok or Err results.

    Returns
    -------
    Sequence[T]
        A sequence of T values from the Ok results.

    """
    return [res.val for res in results if isinstance(res, Ok)]
