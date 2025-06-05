# pyright: reportOverlappingOverload=false
__all__ = [
    "PlotKwargs",
    "close_figure",
    "create_figure",
    "cycler_kwargs",
    "figure_kwargs",
    "legend_kwargs",
    "padding_kwargs",
    "style_kwargs",
    "update_figure_setting",
]

from typing import Literal, Unpack, overload

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .impl import (
    cycler_kwargs,
    figure_kwargs,
    legend_kwargs,
    padding_kwargs,
    style_kwargs,
    update_figure_setting,
)
from .typing import PlotKwargs

def close_figure(fig: Figure | None = None) -> None: ...
@overload
def create_figure(
    **kwargs: Unpack[PlotKwargs],
) -> Figure: ...
@overload
def create_figure(
    ncols: Literal[1],
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Axes]: ...
@overload
def create_figure(
    nrows: Literal[1],
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Axes]: ...
@overload
def create_figure(
    ncols: Literal[1],
    nrows: Literal[1],
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Axes]: ...
@overload
def create_figure(
    ncols: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, tuple[Axes, ...]]: ...
@overload
def create_figure(
    ncols: int,
    nrows: Literal[1],
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, tuple[Axes, ...]]: ...
@overload
def create_figure(
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, tuple[Axes, ...]]: ...
@overload
def create_figure(
    ncols: Literal[1],
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, tuple[Axes, ...]]: ...
@overload
def create_figure(
    ncols: int,
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, tuple[tuple[Axes, ...], ...]]: ...
