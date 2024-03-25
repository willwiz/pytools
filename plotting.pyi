__all__ = ["PlotStyle", "new_fig", "add_axis", "get_axis_lim"]
from typing import Any, Literal, TypedDict
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from cycler import Cycler
from numpy import ndarray as Arr, float64, dtype

f64 = dtype[float64]

class AxesTickSettings(TypedDict):
    axis: Literal["both", "x", "y"]
    labelsize: int

class FigStyleSettings(TypedDict):
    markersize: int
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
    ) -> None: ...

def new_fig(
    fig_size: tuple[float, float] = (4, 3),
    dpi: int = 180,
    style: PlotStyle | None = None,
    fig: Figure | None = None,
): ...
def add_axis(
    fig: Figure,
    style: PlotStyle,
    nrows: int = 1,
    ncols: int = 1,
    index: int = 1,
    projection: Literal["3d"] | None = None,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
) -> Axes: ...
def get_axis_lim(data: Arr[Any, f64], padding: float = 0.02) -> tuple[float, float]: ...
