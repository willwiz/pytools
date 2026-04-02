from functools import wraps
from time import perf_counter
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

# Define type variables to represent any parameters (P) and return type (R)
P = ParamSpec("P")
R = TypeVar("R")


def timeit[**P, R](f: Callable[P, R]) -> Callable[P, R]:
    @wraps(f)
    def wrap(*args: P.args, **kw: P.kwargs) -> R:
        ts = perf_counter()
        result = f(*args, **kw)
        te = perf_counter()
        msg = f"func{f.__name__!r} args:[{args!r}, {kw!r}] took: {te - ts:.4f} sec"
        print(msg)
        return result

    return wrap
