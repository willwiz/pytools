from __future__ import annotations

__all__ = [
    "LEGEND_KEYS",
    "CyclerKwargs",
    "FigureKwargs",
    "FontKwargs",
    "LegendKwargs",
    "PaddingKwargs",
    "PlotKwargs",
    "StyleKwargs",
]

from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Sequence

LEGEND_KEYS = Literal["loc", "handlelength", "frameon", "fontsize", "labelspacing", "columnspacing"]


class PlotKwargs(TypedDict, total=False):
    figsize: tuple[int, int]
    dpi: int
    layout: Literal["constrained"]
    xlabel: str
    ylabel: str
    xlim: tuple[float, float]
    ylim: tuple[float, float]
    curve_labels: Sequence[str]
    color: Sequence[str]
    alpha: Sequence[float]
    linestyle: Sequence[str]
    linewidth: Sequence[float]
    marker: Sequence[str]
    markersize: int | float
    markerskip: int | list[int] | float | list[float]
    markeredgewidth: float
    fillstyle: str
    loc: Literal["outside lower center", "upper right", "lower left", "best"]
    handlelength: float
    frameon: bool
    fontsize: float
    labelspacing: float
    columnspacing: float
    legendlabelcols: int
    padleft: float
    padright: float
    padtop: float
    padbottom: float
    transparency: bool


class LegendKwargs(TypedDict, total=False):
    loc: Literal["outside lower center", "upper right", "lower left", "best"]
    handlelength: float
    frameon: bool
    fontsize: float
    labelspacing: float
    columnspacing: float
    legendlabelcols: int


class CyclerKwargs(TypedDict, total=False):
    color: Sequence[str]
    mec: Sequence[str]
    alpha: Sequence[float]
    linestyle: Sequence[str]
    linewidth: Sequence[float]
    marker: Sequence[str]


class StyleKwargs(TypedDict, total=False):
    markevery: int | Sequence[int] | float | Sequence[float]
    markersize: int | float
    fillstyle: str
    markeredgewidth: float


class FigureKwargs(TypedDict, total=False):
    figsize: tuple[int, int]
    dpi: int
    layout: Literal["constrained"]


class PaddingKwargs(TypedDict, total=False):
    left: float
    right: float
    top: float
    bottom: float
    hspace: float
    wspace: float


class FontKwargs(TypedDict, total=False):
    fontsize: float
