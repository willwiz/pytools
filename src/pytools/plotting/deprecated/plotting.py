# pyright: reportUnknownMemberType=false
from __future__ import annotations

from typing import TYPE_CHECKING, Unpack

import matplotlib.pyplot as plt
import numpy as np

from .fig_configure import get_figure_settings, get_figure_styles, update_figure_setting

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from arraystubs import Vec, flt

    from trabeculae.plotting.data import PlotKwargs


def plot_byrow(
    *data: tuple[Vec[flt], Vec[flt]] | list[Vec[flt]],
    fout: str | Path | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    n_set = len(data)
    opts = get_figure_settings(**kwargs)
    fig, axes = plt.subplots(
        n_set,
        1,
        dpi=opts.dpi,
        figsize=opts.figsize,
        layout=opts.layout,
    )
    update_figure_setting(fig, **kwargs)
    styles = get_figure_styles(**kwargs)

    for k, (x, y) in enumerate(data):
        axes[k].plot(x, y, **styles)

    if fout:
        fig.savefig(fout, transparent=opts.transparency)
    else:
        plt.show()
    plt.close(fig)


def plot_scalar(
    *data: tuple[Vec[flt], Vec[flt]] | list[Vec[flt]],
    fout: str | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    opts = get_figure_settings(**kwargs)
    fig, ax = plt.subplots(1, 1, dpi=opts.dpi, figsize=opts.figsize, layout=opts.layout)
    update_figure_setting(fig, **kwargs)
    styles = get_figure_styles(**kwargs)
    for x, y in data:
        ax.plot(x, y, **styles)
    if fout:
        fig.savefig(fout, transparent=opts.transparency)
    else:
        plt.show()
    plt.close(fig)


def semilogy_plot(
    *data: tuple[Vec[flt], Vec[flt]],
    scale: float = 1.0,
    fout: str | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    opts = get_figure_settings(**kwargs)
    fig, ax = plt.subplots(1, 1, dpi=opts.dpi, figsize=opts.figsize, layout=opts.layout)
    update_figure_setting(fig, **kwargs)
    styles = get_figure_styles(**kwargs)
    for x, y in data:
        ax.semilogy(x, y / scale, **styles)
    if fout:
        fig.savefig(fout, transparent=opts.transparency)
    else:
        plt.show()
    plt.close(fig)


def loglog_plot(
    *data: tuple[Vec[flt], Vec[flt]],
    scale: float = 1.0,
    fout: str | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    opts = get_figure_settings(**kwargs)
    fig, ax = plt.subplots(1, 1, dpi=opts.dpi, figsize=opts.figsize, layout=opts.layout)
    update_figure_setting(fig, **kwargs)
    styles = get_figure_styles(**kwargs)
    for x, y in data:
        ax.loglog(x, y / scale, **styles)
    if fout:
        fig.savefig(fout, transparent=opts.transparency)
    else:
        plt.show()
    plt.close(fig)


def barplot(
    *data: list[float] | Vec[flt],
    dlabel: Sequence[str | int] | None = None,
    xcat: Sequence[str] | None = None,
    color_list: Sequence[str] | None = ["b", "b"],
    title: str | None = None,
    xlabel: str = "Pop size",
    ylabel: str = "Iterations to Convergence",
    dpi: int = 600,
    width: float = 4,
    height: float = 3,
    transparency: bool = False,
    fout: str | None = None,
) -> None:
    fig, ax = plt.subplots(dpi=dpi, figsize=(width, height), layout="constrained")
    nset = len(data)
    bar_width = 1.0 / (nset + 1)
    npoints = len(data[0])
    xticks = np.arange(npoints)
    labels = dlabel if dlabel else [None for _ in range(nset)]
    if xcat is not None:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xcat)
    if title:
        ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    for i, (d, l) in enumerate(zip(data, labels)):
        offset = bar_width * i - (0.5 - bar_width)
        ax.bar(xticks + offset, d, bar_width, color=color_list, label=l)
    if dlabel:
        ax.legend(loc="upper center", ncols=nset)
    if fout is None:
        plt.show()
    else:
        plt.savefig(fout, bbox_inches="tight", transparent=transparency)
    plt.close(fig)
