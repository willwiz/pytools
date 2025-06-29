# pyright: reportUnknownMemberType=false
from __future__ import annotations

from itertools import cycle

from matplotlib.axes import Axes

__all__ = [
    "bar_cycler",
    "close_figure",
    "create_figure",
    "figstyle",
    "update_figure_setting",
]

from typing import TYPE_CHECKING, Any, Unpack

from matplotlib import pyplot as plt

from ._impl_default import cycler_kwargs, figure_kwargs, font_kwargs, legend_kwargs, padding_kwargs

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from .trait import BarCyclerKwargs, BarPlotKwargs, PlotKwargs, StyleKwargs


def create_figure(
    ncols: int | None = None,
    nrows: int | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> (
    tuple[Figure, Axes]
    | tuple[Figure, np.ndarray[tuple[int], Any]]
    | tuple[Figure, np.ndarray[tuple[int, int], Any]]
):
    opts = figure_kwargs(**kwargs)
    _ncols = ncols if ncols is not None else 1
    _nrows = nrows if nrows is not None else 1
    fig, ax = plt.subplots(_nrows, _ncols, squeeze=False, **opts)
    match ncols, nrows:
        case None, None:
            return fig, ax[0, 0]
        case None, _:
            return fig, ax[:, 0]  # type: ignore[return-value]
        case _, None:
            return fig, ax[0, :]  # type: ignore[return-value]
        case _, _:
            return fig, ax
    # matplotlib leave ax as unknown, nothing to do here
    return fig, ax


def close_figure(fig: Figure | None = None) -> None:
    """Close the specified figure or the current active figure."""
    if fig is None:
        plt.close()
    else:
        plt.close(fig)


def figstyle(**kwargs: Unpack[PlotKwargs]) -> StyleKwargs:
    style: StyleKwargs = {}
    if "markevery" in kwargs:
        style["markevery"] = kwargs["markevery"]
    if "markersize" in kwargs:
        style["markersize"] = kwargs["markersize"]
    if "fillstyle" in kwargs:
        style["fillstyle"] = kwargs["fillstyle"]
    if "markeredgewidth" in kwargs:
        style["markeredgewidth"] = kwargs["markeredgewidth"]
    if "width" in kwargs:
        style["width"] = kwargs["width"]
    return style


def bar_cycler(n: int, **kwargs: Unpack[BarPlotKwargs]) -> Sequence[BarCyclerKwargs]:
    hatches: Sequence[BarCyclerKwargs] = [{**figstyle(**kwargs)} for _ in range(n)]
    if "hatch" in kwargs:
        cycler = cycle(kwargs["hatch"])
        for v in hatches:
            v["hatch"] = next(cycler)
    # if "edgecolor" in kwargs:
    #     cycler = cycle(kwargs["edgecolor"])
    #     for v in hatches:
    #         v["edgecolor"] = next(cycler)
    return hatches


def update_figure_setting(fig: Figure, **kwargs: Unpack[PlotKwargs]) -> None:
    if not fig.axes:
        return
    cyclers: dict[str, Any] = {**cycler_kwargs(**kwargs)}
    fig.subplots_adjust(**padding_kwargs(fig, **kwargs))
    for ax in fig.axes:
        if cyclers:
            ax.set_prop_cycle(**cyclers)
        if "fontsize" in kwargs:
            ax.tick_params(axis="both", which="major", labelsize=kwargs["fontsize"] - 2)
        if "curve_labels" in kwargs:
            ax.legend(**legend_kwargs(**kwargs))
        if "xlabel" in kwargs:
            ax.set_xlabel(kwargs["xlabel"], **font_kwargs(**kwargs))
        if "ylabel" in kwargs:
            ax.set_ylabel(kwargs["ylabel"], **font_kwargs(**kwargs))
        if "xlim" in kwargs:
            ax.set_xlim(kwargs["xlim"])
        if "ylim" in kwargs:
            ax.set_ylim(kwargs["ylim"])
