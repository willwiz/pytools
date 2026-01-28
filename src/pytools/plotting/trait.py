from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = [
    "BarPlotKwargs",
    "CyclerKwargs",
    "FigureKwargs",
    "FontKwargs",
    "LegendKeys",
    "LegendKwargs",
    "PaddingKwargs",
    "PlotKwargs",
    "StyleKwargs",
]

LegendKeys = Literal["loc", "handlelength", "frameon", "fontsize", "labelspacing", "columnspacing"]
LegendLocs = Literal["outside lower center", "upper right", "lower left", "best"]


class PlotKwargs(TypedDict, total=False):
    figsize: tuple[float, float]
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
    linewidth: Sequence[float] | float
    edgecolor: Sequence[str]
    facecolor: Sequence[str]
    mec: Sequence[str]
    marker: Sequence[str]
    markersize: int | float
    markevery: int | Sequence[int] | float | Sequence[float]
    markeredgewidth: float
    fillstyle: str
    loc: Literal["outside lower center", "upper right", "lower left", "best"]
    handlelength: float
    frameon: bool
    fontsize: float
    labelspacing: float
    columnspacing: float
    legendlabelcols: int
    title: str
    padleft: float
    padright: float
    padtop: float
    padbottom: float
    hspace: float
    wspace: float
    transparency: bool
    width: float
    hatch: str | Sequence[str]
    head_space: float


class BarPlotKwargs(PlotKwargs, TypedDict, total=False):
    fill: bool
    hatch: Sequence[str]
    edgecolor: Sequence[str]


class LegendKwargs(TypedDict, total=False):
    loc: LegendLocs
    handlelength: float
    frameon: bool
    fontsize: float
    labelspacing: float
    columnspacing: float
    ncols: int


class CyclerKwargs(TypedDict, total=False):
    color: Sequence[str]
    mec: Sequence[str]
    alpha: Sequence[float]
    linestyle: Sequence[str]
    linewidth: Sequence[float]
    marker: Sequence[str]
    hatch: Sequence[str]


class StyleKwargs(TypedDict, total=False):
    markevery: int | float
    markersize: int | float
    fillstyle: str
    markeredgewidth: float
    linewidth: float | int
    width: float
    hatch: str
    edgecolor: str
    color: str
    linestyle: str


class BarCyclerKwargs(CyclerKwargs, TypedDict, total=False):
    hatch: Sequence[str]


class FigureKwargs(TypedDict, total=False):
    figsize: tuple[float, float]
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
