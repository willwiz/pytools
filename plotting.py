from typing import Any, Literal, TypedDict
import numpy as np
import matplotlib.pyplot as plt
from cycler import Cycler, cycler
from matplotlib.figure import Figure
from numpy import ndarray as Arr, float64, dtype
__all__ = ["PlotStyle", "new_fig", "add_axis", "get_axis_lim"]

f64 = dtype[float64]


class AxesTickSettings(TypedDict):
    axis: Literal["both", "x", "y"]
    labelsize: int


class FigStyleSettings(TypedDict):
    markersize: int | float
    markevery: int
    fillstyle: str
    markeredgewidth: float


class PlotStyle:
    __slots__ = ["style", "cyclers", "margins", "axes", "transparent"]
    style: FigStyleSettings
    cyclers: Cycler[str, str]
    margins: dict[str, float | None]
    axes: AxesTickSettings
    transparent: bool

    def __init__(
        self,
        skip: int = 1,
        msize: int | float = 3,
        fillstyle: str = "none",
        mew: float = 0.2,
        colors: list[str] = ["k", "r", "b", "g", "m", "c", "y"],
        lines: list[str] | None = None,
        markers: list[str] | None = None,
        left_margin: float | None = 0.15,
        right_margin: float | None = 0.96,
        bottom_margin: float | None = 0.13,
        top_margin: float | None = 0.96,
        w_space: float | None = None,
        h_space: float | None = None,
        font_size: int = 14,
        transparent: bool = False,
    ) -> None:
        if lines is None:
            lines = ["None"] + (len(colors) - 1) * ["-"]
        if markers is None:
            markers = ["o"] + (len(colors) - 1) * ["None"]
        self.style = {
            "markersize": msize,
            "markevery": skip,
            "fillstyle": fillstyle,
            "markeredgewidth": mew,
        }
        self.cyclers = (
            cycler("color", colors)
            + cycler("linestyle", lines)
            + cycler("marker", markers)
            + cycler("mec", colors)
        )
        self.transparent = transparent
        self.margins = {
            "left": left_margin, "right": right_margin, "top": top_margin,
            "bottom": bottom_margin, "wspace": w_space, "hspace": h_space
        }
        self.axes = {
            "axis": "both",
            "labelsize": font_size
        }


def new_fig(fig_size: tuple[float, float] = (4, 3), dpi: int = 180, style: PlotStyle | None = None, fig: Figure | None = None):
    style = style if style else PlotStyle()
    fig = fig if fig else plt.figure(dpi=dpi)
    fig.clear()
    fig.set_size_inches(*fig_size)
    fig.subplots_adjust(**style.margins)
    return fig


def add_axis(fig: Figure, style: PlotStyle, nrows: int = 1, ncols: int = 1, index: int = 1, projection: Literal["3d"] | None = None, xlim: tuple[float, float] | None = None, ylim: tuple[float, float] | None = None):
    axs = fig.add_subplot(nrows, ncols, index, projection=projection)
    axs.tick_params(**style.axes)
    axs.set_prop_cycle(style.cyclers)
    if xlim:
        axs.set_xlim(xlim)
    if ylim:
        axs.set_ylim(ylim)
    return axs


def get_axis_lim(data: Arr[Any, f64], padding: float = 0.02) -> tuple[float, float]:
    lim = [float(np.min(data)), float(np.max(data))]
    xrange = lim[1] - lim[0]
    return (lim[0] - padding * xrange, lim[1] + padding * xrange)
