from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent import futures
from typing import Any, Protocol, Self, TypedDict, Unpack

from pytools.logging import get_logger

PExecArgs = tuple[Sequence[Any], Mapping[str, Any]]

PExecArgList = Iterable[PExecArgs]


class _SupportNext(Protocol):
    def next(self) -> None: ...


def parallel_exec(
    exe: futures.Executor,
    func: Callable[..., Any],
    args: PExecArgList,
    *,
    prog_bar: _SupportNext | None = None,
) -> None:
    jobs: dict[futures.Future[Any], int] = {}
    logger = get_logger()
    for i, (a, k) in enumerate(args):
        jobs[exe.submit(func, *a, **k)] = i
    for future in futures.as_completed(jobs):
        future.result()
        prog_bar.next() if prog_bar else logger.disp(f"<<< Completed {jobs[future]}")


class ThreadMethods(TypedDict, total=False):
    core: int
    thread: int
    interpreter: int


class ThreadedRunner:
    _exe: futures.Executor
    _futures: dict[futures.Future[Any], int]
    _counter: int
    prog_bar: _SupportNext | None

    def __init__(
        self, *, prog_bar: _SupportNext | None = None, **kwargs: Unpack[ThreadMethods]
    ) -> None:
        if (n := kwargs.get("core")) is not None:
            self._exe = futures.ProcessPoolExecutor(n)
        elif (n := kwargs.get("thread")) is not None:
            self._exe = futures.ThreadPoolExecutor(n)
        elif (n := kwargs.get("interpreter")) is not None:
            self._exe = futures.ProcessPoolExecutor(n)
        else:
            self._exe = futures.ThreadPoolExecutor(1)
        self._futures = {}
        self._counter = 0
        self.prog_bar = prog_bar

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_args: object) -> None:
        self.wait_then_shutdown()

    def submit(self, func: Callable[..., Any], *args: object, **kwargs: object) -> None:
        self._counter += 1
        self._futures[self._exe.submit(func, *args, **kwargs)] = self._counter

    def wait_then_shutdown(self) -> None:
        logger = get_logger()
        for future in futures.as_completed(self._futures):
            future.result()
            self.prog_bar.next() if self.prog_bar else logger.disp(
                f"<<< Completed {self._futures[future]}"
            )
        self._exe.shutdown()
