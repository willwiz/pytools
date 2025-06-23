# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

__all__ = [
    "cycler_kwargs",
    "figure_kwargs",
    "legend_kwargs",
    "padding_kwargs",
]

from typing import TYPE_CHECKING, Unpack

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from .trait import (
        CyclerKwargs,
        FigureKwargs,
        FontKwargs,
        LegendKwargs,
        PaddingKwargs,
        PlotKwargs,
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
