from __future__ import annotations

import argparse
import dataclasses as dc
import enum
from pathlib import Path


class _ProgramMode(enum.StrEnum):
    APP = "APP"
    LIB = "LIB"


@dc.dataclass(slots=True)
class _ParsedArguments:
    folder: Path
    mode: _ProgramMode


_parser = argparse.ArgumentParser("init", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
_parser.add_argument("--folder", "-f", type=Path, help="Folder in which to initialize the module.")
_mode = _parser.add_mutually_exclusive_group()
_mode.add_argument(
    "--app",
    action="store_const",
    const=_ProgramMode.APP,
    dest="mode",
    help="Initialize as an app.",
)
_mode.add_argument(
    "--lib",
    action="store_const",
    const=_ProgramMode.LIB,
    dest="mode",
    help="Initialize as a library.",
)


_APP_FILES = [
    "__init__.py",
    "__main__.py",
    "_argparse.py",
    "_types.py",
    "types.py",
    "api.py",
    "py.typed",
]

_LIB_FILES = [
    "__init__.py",
    "_types.py",
    "types.py",
    "api.py",
    "py.typed",
]


def parse_args(args: list[str] | None = None) -> _ParsedArguments:
    return _parser.parse_args(args=args, namespace=_ParsedArguments(Path(), _ProgramMode.APP))


def main(folder: Path, mode: _ProgramMode) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    match mode:
        case _ProgramMode.APP:
            files = _APP_FILES
        case _ProgramMode.LIB:
            files = _LIB_FILES
    for file in files:
        (folder / file).touch()


if __name__ == "__main__":
    args = parse_args()
    main(args.folder or Path(), args.mode)
