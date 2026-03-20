from collections.abc import Generator, Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

type _PackedValues[T] = (
    Mapping[Any, Mapping[Any, T]]
    | Mapping[Any, Sequence[T]]
    | Sequence[Mapping[Any, T]]
    | Sequence[Sequence[T]]
    | Generator[Mapping[Any, T]]
    | Generator[Sequence[T]]
)

class IterateAsPath:
    def __init__(self, files: Sequence[str]) -> None: ...
    def __iter__(self) -> Generator[Path]: ...

def clear_dir(folder: Path | str, *pattern: str, exist_ok: bool = True) -> None: ...
def expand_as_path(files: Iterable[str | Path]) -> Sequence[Path]: ...
def iter_unpack[T: Any](var: _PackedValues[T]) -> Generator[T]: ...
