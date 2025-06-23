__all__ = [
    "bar_cycler",
    "close_figure",
    "create_figure",
    "figstyle",
    "update_figure_setting",
]

from collections.abc import Sequence
from typing import Unpack, overload

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .trait import BarCyclerKwargs, BarPlotKwargs, PlotKwargs, StyleKwargs

def close_figure(fig: Figure | None = None) -> None: ...
@overload
def create_figure(
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Axes]: ...
@overload
def create_figure(
    ncols: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Sequence[Axes]]: ...
@overload
def create_figure(
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Sequence[Axes]]: ...
@overload
def create_figure(
    ncols: int,
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Sequence[Sequence[Axes]]]: ...
def update_figure_setting(
    fig: Figure,
    **kwargs: Unpack[PlotKwargs],
) -> None: ...
def figstyle(**kwargs: Unpack[PlotKwargs]) -> StyleKwargs: ...
def bar_cycler(n: int, **kwargs: Unpack[BarPlotKwargs]) -> Sequence[BarCyclerKwargs]: ...
