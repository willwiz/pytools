from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TextIO

from ._string_parse import filter_ansi
from ._trait import IHandler


class FileHandler(IHandler):
    __slots__ = ("_f",)
    _f: TextIO

    def __init__(self, file: Path | str) -> None:
        file = Path(file)
        self._f = file.open("a", encoding="utf-8")

    def __del__(self) -> None:
        self._f.close()

    def __repr__(self) -> str:
        return f"<FileHandler: {self._f.name}>"

    def log(self, msg: str) -> None:
        self._f.write(filter_ansi(msg).replace("\r", "\n"))
        self.flush()

    def flush(self) -> None:
        self._f.flush()
        os.fsync(self._f.fileno())


class _STDOUTHandler(IHandler):
    def __init__(self) -> None:
        pass

    def __del__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "<STDOUTHandler: sys.stdout>"

    def log(self, msg: str) -> None:
        sys.stdout.write(msg)

    def flush(self) -> None:
        sys.stdout.flush()


STDOUT_HANDLER = _STDOUTHandler()
