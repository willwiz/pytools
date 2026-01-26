from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from warnings import deprecated

from pytools.logging import NLOGGER, ILogger

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence


@deprecated("Use pathlib.Path directly instead.")
def path(*v: str | None) -> str:
    """Join args as a system path str."""
    return str(Path(*[s for s in v if s]))


def clear_dir(
    folder: Path | str, *pattern: str, exist_ok: bool = True, log: ILogger = NLOGGER
) -> None:
    """Remove all files in directory with suffixes.

    If no suffix is given, all files are removed.
    """
    folder = Path(folder)
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
        log.warn(msg)


def expand_as_path(files: Sequence[str]) -> Sequence[Path]:
    """Expand user and vars in path."""
    return [Path(f) for name in files for f in Path().glob(name)]


def expanded_path_generator(files: Sequence[str]) -> Generator[Path]:
    return (Path(f) for name in files for f in Path().glob(name))
