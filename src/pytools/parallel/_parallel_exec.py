from collections.abc import Callable, Collection, Mapping, Sequence
from concurrent import futures
from typing import Any

from pytools.progress import ProgressBar

PEXEC_ARGS = Collection[tuple[Sequence[Any], Mapping[str, Any]]]


def parallel_exec(
    exe: futures.Executor,
    func: Callable[..., Any],
    args: PEXEC_ARGS,
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
