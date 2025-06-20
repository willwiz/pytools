from __future__ import annotations

import warnings
from pathlib import Path
from typing import TYPE_CHECKING

from pytools.logging.api import NULL_LOGGER

if TYPE_CHECKING:
    from pytools.logging.trait import ILogger

warnings.warn("deprecated", DeprecationWarning, stacklevel=2)


def path(*v: str | None) -> str:
    """Join args as a system path str."""
    return str(Path(*[s for s in v if s]))


def clear_dir(folder: Path | str, *suffix: str, log: ILogger = NULL_LOGGER) -> None:
    """Remove all files in directory with suffixes."""
    folder = Path(folder)
    if not folder.is_dir():
        log.warn(f"Dir {folder} was not found.")
        folder.mkdir(parents=True, exist_ok=True)
    if len(suffix) == 0:
        [v.unlink() for v in folder.glob("*") if v.is_file()]
        return
    [v.unlink() for s in suffix for v in folder.glob(f"*.{s}") if v.is_file()]
