from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from warnings import deprecated

from pytools.logging.api import NLOGGER

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pytools.logging.trait import ILogger


@deprecated("Use pathlib.Path directly instead.")
def path(*v: str | None) -> str:
    """Join args as a system path str."""
    return str(Path(*[s for s in v if s]))


def clear_dir(folder: Path | str, *suffix: str, log: ILogger = NLOGGER) -> None:
    """Remove all files in directory with suffixes.

    If no suffix is given, all files are removed.
    """
    folder = Path(folder)
    if not folder.is_dir():
        log.warn(f"Dir {folder} was not found.")
        folder.mkdir(parents=True, exist_ok=True)
    if len(suffix) == 0:
        [v.unlink() for v in folder.glob("*") if v.is_file()]
        return
    [v.unlink() for s in suffix for v in folder.glob(f"*.{s}") if v.is_file()]


def expand_as_path(files: Sequence[str]) -> Sequence[Path]:
    """Expand user and vars in path."""
    return [Path(f) for name in files for f in Path().glob(name)]
