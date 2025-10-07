__all__ = [
    "LEGEND_KEYS",
    "BarPlotKwargs",
    "CyclerKwargs",
    "FigureKwargs",
    "FontKwargs",
    "LegendKwargs",
    "PaddingKwargs",
    "PlotKwargs",
    "StyleKwargs",
]

from collections.abc import Sequence
from typing import Literal, TypedDict

type LEGEND_KEYS = Literal[
    "loc",
    "handlelength",
    "frameon",
    "fontsize",
    "labelspacing",
    "columnspacing",
]

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
    padleft: float
    padright: float
    padtop: float
    padbottom: float
    hspace: float
    wspace: float
    transparency: bool

class BarPlotKwargs(PlotKwargs, TypedDict, total=False):
    fill: bool
    hatch: Sequence[str]
    edgecolor: Sequence[str]

class LegendKwargs(TypedDict, total=False):
    loc: Literal["outside lower center", "upper right", "lower left", "best"]
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

class BarCyclerKwargs(CyclerKwargs, TypedDict, total=False):
    hatch: Sequence[str]

class StyleKwargs(TypedDict, total=False):
    markevery: int | Sequence[int] | float | Sequence[float]
    markersize: int | float
    fillstyle: str
    markeredgewidth: float
    width: float
    linewidth: float

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
