__all__ = ["PEXEC_ARGS", "parallel_exec"]
from collections.abc import Collection, Mapping, Sequence
from concurrent import futures
from typing import Any, Callable

import typing_extensions

PEXEC_ARGS: typing_extensions.TypeAlias = Collection[tuple[Sequence[Any], Mapping[str, Any]]]

def parallel_exec(
    exe: futures.ProcessPoolExecutor,
    func: Callable[..., Any],
    args: Collection[tuple[Sequence[Any], Mapping[str, Any]]],
    prog_bar: bool = False,
) -> None: ...
