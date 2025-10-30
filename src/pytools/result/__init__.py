import inspect
import types
from typing import Any


class Okay[T: Any]:
    __slots__ = ("val",)
    __match_args__ = ("val",)
    val: T

    def __init__(self, value: T) -> None:
        self.val = value


class Err:
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
