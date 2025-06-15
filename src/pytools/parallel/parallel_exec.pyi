__all__ = ["PEXEC_ARGS", "parallel_exec"]
from collections.abc import Callable, Collection, Mapping, Sequence
from concurrent import futures
from typing import Any

type PEXEC_ARGS = Collection[tuple[Sequence[Any], Mapping[str, Any]]]

def parallel_exec(
    exe: futures.ProcessPoolExecutor,
    func: Callable[..., Any],
    args: Collection[tuple[Sequence[Any], Mapping[str, Any]]],
    prog_bar: bool = False,
) -> None: ...
