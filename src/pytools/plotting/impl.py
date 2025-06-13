# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

from itertools import cycle

__all__ = [
    "bar_cycler_kwargs",
    "bar_cycler_kwargs",
    "cycler_kwargs",
    "figure_kwargs",
    "legend_kwargs",
    "padding_kwargs",
    "style_kwargs",
    "update_figure_setting",
]

from typing import TYPE_CHECKING, Any, Unpack

if TYPE_CHECKING:
    from collections.abc import Sequence

    from matplotlib.figure import Figure

    from .typing import (
        BarCyclerKwargs,
        BarPlotKwargs,
        CyclerKwargs,
        FigureKwargs,
        FontKwargs,
        LegendKwargs,
        PaddingKwargs,
        PlotKwargs,
        StyleKwargs,
    )


def font_kwargs(**kwargs: Unpack[PlotKwargs]) -> FontKwargs:
    return {"fontsize": kwargs.get("fontsize", 14)}


def legend_kwargs(**kwargs: Unpack[PlotKwargs]) -> LegendKwargs:
    return {
        "loc": kwargs.get("loc", "outside lower center"),
        "handlelength": kwargs.get("handlelength", 1.0),
        "frameon": kwargs.get("frameon", False),
        "fontsize": kwargs.get("fontsize", 9),
        "labelspacing": kwargs.get("labelspacing", 0.25),
        "columnspacing": kwargs.get("columnspacing", 1.0),
        "legendlabelcols": kwargs.get("legendlabelcols", 4),
    }


def cycler_kwargs(**kwargs: Unpack[PlotKwargs]) -> CyclerKwargs:
    cycler: CyclerKwargs = {}
    if "color" in kwargs:
        cycler["color"] = kwargs["color"]
    if "mec" in kwargs:
        cycler["mec"] = kwargs["mec"]
    if "alpha" in kwargs:
        cycler["alpha"] = kwargs["alpha"]
    if "linestyle" in kwargs:
        cycler["linestyle"] = kwargs["linestyle"]
    if "linewidth" in kwargs:
        cycler["linewidth"] = kwargs["linewidth"]
    if "marker" in kwargs:
        cycler["marker"] = kwargs["marker"]
    return cycler


def style_kwargs(**kwargs: Unpack[PlotKwargs]) -> StyleKwargs:
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


def figure_kwargs(**kwargs: Unpack[PlotKwargs]) -> FigureKwargs:
    figure: FigureKwargs = {
        "figsize": kwargs.get("figsize", (4, 3)),
        "dpi": kwargs.get("dpi", 180),
    }
    if "layout" in kwargs:
        figure["layout"] = kwargs["layout"]
    return figure


def padding_kwargs(fig: Figure, **kwargs: Unpack[PlotKwargs]) -> PaddingKwargs:
    if "layout" in kwargs:
        return {}
    width, height = fig.get_size_inches()
    ratio = width / height
    left = kwargs.get("padleft", 0.15)
    if "ylabel" in kwargs:
        left = 1.5 * left
    bottom = kwargs.get("padbottom", 0.1)
    if "xlabel" in kwargs:
        bottom = bottom + 0.5 * left
    right = kwargs.get("padright", 0.02) / ratio
    top = kwargs.get("padtop", 0.02)
    if not fig.axes:
        return {"left": left, "right": right, "top": top, "bottom": bottom}
    grid = fig.axes[0].get_gridspec()
    if grid is None:
        return {"left": left, "right": right, "top": top, "bottom": bottom}
    hspace = top + bottom
    wspace = left + right
    left = left / grid.ncols
    right = right / grid.ncols
    top = top / grid.nrows
    bottom = bottom / grid.nrows
    right = 1.0 - right
    top = 1.0 - top
    return {
        "left": left,
        "right": right,
        "top": top,
        "bottom": bottom,
        "hspace": hspace,
        "wspace": wspace,
    }


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


def bar_cycler_kwargs(n: int, **kwargs: Unpack[BarPlotKwargs]) -> Sequence[BarCyclerKwargs]:
    hatches: Sequence[BarCyclerKwargs] = [{**style_kwargs(**kwargs)} for _ in range(n)]
    if "hatch" in kwargs:
        cycler = cycle(kwargs["hatch"])
        for v in hatches:
            v["hatch"] = next(cycler)
    # if "edgecolor" in kwargs:
    #     cycler = cycle(kwargs["edgecolor"])
    #     for v in hatches:
    #         v["edgecolor"] = next(cycler)
    return hatches
