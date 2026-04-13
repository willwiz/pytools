from collections.abc import Callable
from concurrent.futures import Future
from typing import Protocol, Self, TypedDict, Unpack

class _SupportNext(Protocol):
    def next(self) -> None: ...

class ThreadMethods(TypedDict, total=False):
    core: int
    thread: int
    interpreter: int

class ThreadedRunner:
    def __init__(
        self, *, prog_bar: _SupportNext | None = None, **kwargs: Unpack[ThreadMethods]
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *_args: object) -> None: ...
    def submit[**P, R](
        self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> Future[R]: ...
    def wait_then_shutdown(self) -> None: ...
