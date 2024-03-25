__all__ = ["ProgressBar"]

from typing import Literal as L

class ProgressBar:
    def __init__(
        self,
        max: int,
        prefix: str = "",
        suffix: str = "",
        length: int = 40,
        decimal: int = 1,
        pixel: str = "*",
        end: L["\n", "\r", ""] = "",
    ) -> None: ...
    def reset(self) -> None: ...
    def next(self) -> None: ...
    def finish(self) -> None: ...
