# pyright: reportUnknownMemberType=false
import dataclasses as dc
from typing import Unpack

import matplotlib.figure as mplf
import matplotlib.pyplot as plt

from .data import FigureSettings, PlotCyclers, PlotKwargs, PlotStyles


def get_figure_settings(**kwargs: Unpack[PlotKwargs]):
    settings = FigureSettings()
    if "figsize" in kwargs:
        settings.figsize = kwargs["figsize"]
    if "dpi" in kwargs:
        settings.dpi = kwargs["dpi"]
    if "layout" in kwargs:
        settings.layout = kwargs["layout"]
    if "transparency" in kwargs:
        settings.transparency = kwargs["transparency"]
    return settings


def get_figure_styles(**kwargs: Unpack[PlotKwargs]):
    styles: PlotStyles = {
        "markersize": 4,
        "markevery": None,
        "fillstyle": "full",
        "markeredgewidth": 0.3,
    }
    if "markersize" in kwargs:
        styles["markersize"] = kwargs["markersize"]
    if "markerskip" in kwargs:
        styles["markevery"] = kwargs["markerskip"]
    if "fillstyle" in kwargs:
        styles["fillstyle"] = kwargs["fillstyle"]
    if "markeredgewidth" in kwargs:
        styles["markeredgewidth"] = kwargs["markeredgewidth"]
    return styles


def create_cyclers(
    **kwargs: Unpack[PlotKwargs],
) -> PlotCyclers:
    cyclers = PlotCyclers()
    if "color" in kwargs:
        cyclers.color = kwargs["color"]
        cyclers.mec = kwargs["color"]
    if "alpha" in kwargs:
        cyclers.alpha = kwargs["alpha"]
    if "linestyle" in kwargs:
        cyclers.linestyle = kwargs["linestyle"]
    if "linewidth" in kwargs:
        cyclers.linewidth = kwargs["linewidth"]
    if "marker" in kwargs:
        cyclers.marker = kwargs["marker"]
    return cyclers


def update_figure_setting(fig: mplf.Figure, **kwargs: Unpack[PlotKwargs]) -> None:
    cyclers = {k: v for k, v in dc.asdict(create_cyclers(**kwargs)).items() if v is not None}
    legendlabelcols = kwargs["legendlabelcols"] if "legendlabelcols" in kwargs else 4
    for ax in fig.axes:
        ax.set_prop_cycle(**cyclers)
    if "x_label" in kwargs:
        match kwargs["x_label"]:
            case str(x_label):
                for ax in fig.axes:
                    ax.set_xlabel(x_label, fontsize=12)
            case list(x_label):
                for ax, label in zip(fig.axes, x_label):
                    ax.set_xlabel(label, fontsize=12)
            case _:
                raise ValueError("x_label must be a string or a list of strings")
    if "y_label" in kwargs:
        match kwargs["y_label"]:
            case str(y_label):
                for ax in fig.axes:
                    ax.set_ylabel(y_label, fontsize=12)
            case list(y_label):
                for ax, label in zip(fig.axes, y_label):
                    ax.set_ylabel(label, fontsize=12)
            case _:
                raise ValueError("y_label must be a string or a list of strings")
    if "curve_labels" in kwargs:
        fig.legend(kwargs["curve_labels"], ncols=legendlabelcols, **LEGEND_KWARGS)
    if "x_lim" in kwargs:
        plt.setp(fig.axes, xlim=kwargs["x_lim"])
    if "y_lim" in kwargs:
        plt.setp(fig.axes, ylim=kwargs["y_lim"])
