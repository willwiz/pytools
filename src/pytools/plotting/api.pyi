from collections.abc import Sequence
from typing import Unpack, overload

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .trait import BarCyclerKwargs, BarPlotKwargs, LegendKwargs, PlotKwargs, StyleKwargs

__all__ = [
    "bar_cycler",
    "close_figure",
    "create_figure",
    "legend_kwargs",
    "style_kwargs",
    "update_axis_setting",
    "update_figure_setting",
]

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
    nrows: int,
    ncols: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Sequence[Sequence[Axes]]]: ...
def update_figure_setting(
    fig: Figure,
    **kwargs: Unpack[PlotKwargs],
) -> None: ...
def update_axis_setting(
    ax: Axes,
    **kwargs: Unpack[PlotKwargs],
) -> None: ...
def style_kwargs(**kwargs: Unpack[PlotKwargs]) -> StyleKwargs: ...
def bar_cycler(n: int, **kwargs: Unpack[BarPlotKwargs]) -> Sequence[BarCyclerKwargs]: ...
def legend_kwargs(**kwargs: Unpack[PlotKwargs]) -> LegendKwargs: ...
