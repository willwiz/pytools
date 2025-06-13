# pyright: reportOverlappingOverload=false
__all__ = [
    "PlotKwargs",
    "bar_cycler_kwargs",
    "close_figure",
    "create_figure",
    "cycler_kwargs",
    "figure_kwargs",
    "legend_kwargs",
    "padding_kwargs",
    "style_kwargs",
    "update_figure_setting",
]

from collections.abc import Sequence
from typing import Unpack, overload

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .impl import (
    bar_cycler_kwargs,
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
