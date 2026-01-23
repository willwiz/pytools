from __future__ import annotations

from collections.abc import Iterable
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

__all__ = [
    "cycler_kwargs",
    "figure_kwargs",
    "legend_kwargs",
    "padding_kwargs",
]


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
        "ncols": kwargs.get("legendlabelcols", 4),
    }


def cycler_kwargs(**kwargs: Unpack[PlotKwargs]) -> CyclerKwargs:
    cycler: CyclerKwargs = {}
    color = kwargs.get("color")
    if isinstance(color, Iterable) and not isinstance(color, str):
        cycler["color"] = color
    mec = kwargs.get("mec")
    if isinstance(mec, Iterable) and not isinstance(mec, str):
        cycler["mec"] = mec
    alpha = kwargs.get("alpha")
    if isinstance(alpha, Iterable):
        cycler["alpha"] = alpha
    linestyle = kwargs.get("linestyle")
    if isinstance(linestyle, Iterable) and not isinstance(linestyle, str):
        cycler["linestyle"] = linestyle
    marker = kwargs.get("marker")
    if isinstance(marker, Iterable) and not isinstance(marker, str):
        cycler["marker"] = marker
    linewidth = kwargs.get("linewidth")
    if isinstance(linewidth, Iterable):
        cycler["linewidth"] = linewidth
    hatch = kwargs.get("hatch")
    if isinstance(hatch, (str, Iterable)) and not isinstance(hatch, str):
        cycler["hatch"] = hatch
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
    head_space: float = kwargs.get("head_space", 0.0)
    width, height = fig.get_size_inches()
    height = height - head_space * height
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
    top = top + 0.5 * head_space
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
