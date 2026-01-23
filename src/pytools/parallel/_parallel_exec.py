from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent import futures
from typing import Any, Protocol

PEXEC_ARGS = Iterable[tuple[Sequence[Any], Mapping[str, Any]]]


class _SupportNext(Protocol):
    def next(self) -> None: ...


def parallel_exec(
    exe: futures.Executor,
    func: Callable[..., Any],
    args: PEXEC_ARGS,
    *,
    prog_bar: _SupportNext | None = None,
) -> None:
    jobs: dict[futures.Future[Any], int] = {}
    for i, (a, k) in enumerate(args):
        jobs[exe.submit(func, *a, **k)] = i
    for future in futures.as_completed(jobs):
        future.result()
        prog_bar.next() if prog_bar else print(f"<<< Completed {jobs[future]}")
