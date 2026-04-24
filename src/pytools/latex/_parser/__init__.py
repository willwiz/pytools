from ._highlight import hl_parser, parse_highlight_args
from ._merge import merge_parser, parse_merge_args
from ._types import HighlightKwargs, MergeKwargs

__all__ = [
    "HighlightKwargs",
    "MergeKwargs",
    "hl_parser",
    "merge_parser",
    "parse_highlight_args",
    "parse_merge_args",
]
