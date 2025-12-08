import abc
import inspect
import types
from collections.abc import Sequence
from typing import Any, Never, TypeGuard

__all__ = ["Err", "Ok"]


class _ResultType[T: Any](abc.ABC):
    @abc.abstractmethod
    def unwrap(self) -> T:
        pass

    @abc.abstractmethod
    def unwrap_or[O: Any](self, default: O, /) -> T | O:
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


def all_ok[T](results: Sequence[Ok[T] | Err]) -> TypeGuard[Sequence[Ok[T]]]:
    return all(isinstance(res, Ok) for res in results)
