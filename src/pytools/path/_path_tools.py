from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar, cast
from warnings import deprecated

from pytools.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import Generator


@deprecated("Use pathlib.Path directly instead.")
def path(*v: str | None) -> str:
    """Join args as a system path str."""
    return str(Path(*[s for s in v if s]))


def clear_dir(folder: Path | str, *pattern: str, exist_ok: bool = True) -> None:
    """Remove all files in directory with suffixes.

    If no suffix is given, all files are removed.
    """
    folder = Path(folder)
    log = get_logger()
    if not folder.is_dir():
        log.warn(f"Dir {folder} was not found.")
        folder.mkdir(parents=True, exist_ok=exist_ok)
    if len(pattern) == 0:
        [v.unlink() for v in folder.glob("*") if v.is_file()]
        return
    # valid_sfx = {s: s.startswith(".") for s in suffix}
    # if not all(valid_sfx.values()):
    #     invalid = [s for s, valid in valid_sfx.items() if not valid]
    #     msg = f"Suffixes must start with a dot. Invalid suffixes ignored: {invalid}"
    #     log.warn(msg)
    removed = [v.unlink() for s in pattern for v in folder.glob(f"{s}") if v.is_file()]
    if len(removed) == 0:
        msg = f"No files with patterns {pattern} found in dir {folder} to remove."
        log.debug(msg)


def expand_as_path(files: Sequence[str]) -> Sequence[Path]:
    """Expand user and vars in path."""
    return [Path(f) for name in files for f in Path().glob(name)]


# def iterate_as_path(files: Sequence[str]) -> Generator[Path]:
#     for name in files:
#         for f in Path().glob(name):
#             yield Path(f)


class IterateAsPath:
    def __init__(self, files: Sequence[str]) -> None:
        self.files = files

    def __iter__(self) -> Generator[Path]:
        for name in self.files:
            for f in Path().glob(name):
                yield Path(f)


_T = TypeVar("_T", bound=object, covariant=False)

IterableValues = (
    Mapping[Any, "IterableValues[_T]"]
    | Sequence["IterableValues[_T]"]
    | Mapping[Any, _T]
    | Sequence[_T]
    | _T
)


def iter_unpack(var: IterableValues[_T]) -> Generator[_T]:
    match var:
        case str():
            yield var
        case Mapping():
            var = cast("Mapping[Any, IterableValues[_T]]|Mapping[Any, _T]", var)
            for v in var.values():
                yield from iter_unpack(v)
        case Sequence():
            var = cast("Sequence[IterableValues[_T]]|Sequence[_T]", var)
            for v in var:
                yield from iter_unpack(v)
        case _:
            yield var
