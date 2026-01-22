from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trait import CyclerKwargs, FigureKwargs, LegendKwargs

__all__ = [
    "CYCLER_DEFAULT",
    "FIGURE_DEFAULT",
    "LEGEND_DEFAULT",
    "STYLE_DEFAULT",
]

LEGEND_DEFAULT: LegendKwargs = {
    "loc": "outside lower center",
    "handlelength": 1.0,
    "frameon": False,
    "fontsize": 9,
    "labelspacing": 0.25,
    "columnspacing": 1.0,
}

CYCLER_DEFAULT: CyclerKwargs = {}
STYLE_DEFAULT: CyclerKwargs = {}
FIGURE_DEFAULT: FigureKwargs = {}
