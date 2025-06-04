# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

__all__ = [
    "cycler_kwargs",
    "figure_kwargs",
    "legend_kwargs",
    "padding_kwargs",
    "style_kwargs",
    "update_figure_setting",
]

from typing import TYPE_CHECKING, Any, Unpack

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from .typing import (
        CyclerKwargs,
        FigureKwargs,
        LegendKwargs,
        PaddingKwargs,
        PlotKwargs,
        StyleKwargs,
    )


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
    left = kwargs.get("padleft", 0.15)
    bottom = kwargs.get("padbottom", 0.1)
    right = 1.0 - kwargs.get("padright", 0.1)
    top = 1.0 - kwargs.get("padtop", 0.1)
    if not fig.axes:
        return {"left": left, "right": right, "top": top, "bottom": bottom}
    grid = fig.axes[0].get_gridspec()
    if grid is None:
        return {"left": left, "right": right, "top": top, "bottom": bottom}
    left = left / grid.ncols
    right = right / grid.ncols
    top = top / grid.nrows
    bottom = bottom / grid.nrows
    return {
        "left": left,
        "right": right,
        "top": top,
        "bottom": bottom,
        "hspace": left + right,
        "wspace": top + bottom,
    }


def update_figure_setting(fig: Figure, **kwargs: Unpack[PlotKwargs]) -> None:
    if not fig.axes:
        return
    cyclers: dict[str, Any] = {**cycler_kwargs(**kwargs)}
    for ax in fig.axes:
        ax.set_prop_cycle(**cyclers)
        if "curve_labels" in kwargs:
            ax.legend(**legend_kwargs(**kwargs))
        if "xlabel" in kwargs:
            ax.set_xlabel(kwargs["xlabel"])
        if "ylabel" in kwargs:
            ax.set_ylabel(kwargs["ylabel"])
        if "xlim" in kwargs:
            ax.set_xlim(kwargs["xlim"])
        if "ylim" in kwargs:
            ax.set_ylim(kwargs["ylim"])
