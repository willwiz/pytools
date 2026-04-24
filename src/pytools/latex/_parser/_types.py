from typing import TYPE_CHECKING, Required, TypedDict

if TYPE_CHECKING:
    from pathlib import Path


class MergeKwargs(TypedDict, total=False):
    out: Required[Path]
    clear: bool


class HighlightKwargs(TypedDict, total=False):
    out: Required[Path]
