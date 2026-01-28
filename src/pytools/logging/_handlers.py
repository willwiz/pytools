from __future__ import annotations

import os
import sys
import threading
from pathlib import Path
from typing import TextIO

from ._string_parse import filter_ansi, now
from ._trait import IHandler


class FileHandler(IHandler):
    __slots__ = ("_f", "_lock")
    _f: TextIO
    _lock: threading.Lock

    def __init__(self, file: Path | str) -> None:
        file = Path(file)
        self._f = file.open("a", encoding="utf-8")
        self._f.write(f"Log file created at {now()}\n")
        self._f.write(f"Logger instance: {self!r}\n")
        self._lock = threading.Lock()

    def __del__(self) -> None:
        self._f.write(f"\n\nLog file closed at {now()}\n")
        self._f.close()

    def __repr__(self) -> str:
        return f"<FileHandler: {self._f.name}>"

    def log(self, msg: str) -> None:
        with self._lock:
            self._f.write(filter_ansi(msg).replace("\r", "\n"))
            self.flush()

    def flush(self) -> None:
        with self._lock:
            self._f.flush()
            os.fsync(self._f.fileno())


class STDOUTHandler(IHandler):
    def __init__(self) -> None:
        sys.stdout.write(f"Logger instance: {self!r} created at {now()}\n")

    def __del__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"<STDOUTHandler: {id(self)}>"

    def log(self, msg: str) -> None:
        sys.stdout.write(msg)

    def flush(self) -> None:
        sys.stdout.flush()


STDOUT_HANDLER = STDOUTHandler()
