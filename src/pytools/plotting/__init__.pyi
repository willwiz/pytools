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

from typing import Any, Literal, Unpack, overload

import numpy as np
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
    ncols: None,
    nrows: None,
    **kwargs: Unpack[PlotKwargs],
) -> Figure: ...
@overload
def create_figure(
    ncols: Literal[1] = 1,
    nrows: Literal[1] = 1,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, Axes]: ...
@overload
def create_figure(
    ncols: int,
    nrows: None,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, np.ndarray[tuple[int, int], Any]]: ...
@overload
def create_figure(
    ncols: None,
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, np.ndarray[tuple[int, int], Any]]: ...
@overload
def create_figure(
    ncols: int,
    nrows: int,
    **kwargs: Unpack[PlotKwargs],
) -> tuple[Figure, np.ndarray[tuple[int, int], Any]]: ...
