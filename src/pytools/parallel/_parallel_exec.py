from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent import futures
from typing import Any, Literal, Protocol, Self

PEXEC_ARGS = tuple[Sequence[Any], Mapping[str, Any]]

PEXEC_ARG_LIST = Iterable[PEXEC_ARGS]


class _SupportNext(Protocol):
    def next(self) -> None: ...


def parallel_exec(
    exe: futures.Executor,
    func: Callable[..., Any],
    args: PEXEC_ARG_LIST,
    *,
    prog_bar: _SupportNext | None = None,
) -> None:
    jobs: dict[futures.Future[Any], int] = {}
    for i, (a, k) in enumerate(args):
        jobs[exe.submit(func, *a, **k)] = i
    for future in futures.as_completed(jobs):
        future.result()
        prog_bar.next() if prog_bar else print(f"<<< Completed {jobs[future]}")


class ThreadedRunner:
    _exe: futures.Executor
    _futures: dict[futures.Future[Any], int]
    _counter: int
    prog_bar: _SupportNext | None

    def __init__(
        self,
        cores: int,
        mode: Literal["thread", "core"] = "core",
        prog_bar: _SupportNext | None = None,
    ) -> None:
        match mode:
            case "thread":
                self._exe = futures.ThreadPoolExecutor(cores)
            case "core":
                self._exe = futures.ProcessPoolExecutor(cores)
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
        for future in futures.as_completed(self._futures):
            future.result()
            self.prog_bar.next() if self.prog_bar else print(
                f"<<< Completed {self._futures[future]}"
            )
        self._exe.shutdown()
