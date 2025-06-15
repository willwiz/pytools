__all__ = ["PEXEC_ARGS", "parallel_exec"]
from collections.abc import Callable, Collection
from concurrent import futures
from typing import Any

from pytools.progress import ProgressBar

PEXEC_ARGS = Collection[tuple[list[Any], dict[str, Any]]]


def parallel_exec(
    exe: futures.ProcessPoolExecutor,
    func: Callable[..., Any],
    args: Collection[tuple[list[Any], dict[str, Any]]],
    *,
    prog_bar: bool = False,
) -> None:
    jobs: dict[futures.Future[Any], int] = {}
    bart = ProgressBar(len(args)) if prog_bar else None
    for i, (a, k) in enumerate(args):
        jobs[exe.submit(func, *a, **k)] = i
    for future in futures.as_completed(jobs):
        future.result()
        bart.next() if bart else print(f"<<< Completed {jobs[future]}")
