# pyright: reportUnknownMemberType=false
from __future__ import annotations

from typing import TYPE_CHECKING, Unpack

import matplotlib.pyplot as plt

from .fig_configure import get_figure_settings, get_figure_styles, update_figure_setting

if TYPE_CHECKING:
    from pathlib import Path

    from arraystubs import Vec, flt

    from .data import PlotKwargs


def semilog_plot(
    *data: tuple[Vec[flt], Vec[flt]],
    scale: float = 1.0,
    ylim: tuple[float, float] | None = None,
    fout: str | Path | None = None,
    **kwargs: Unpack[PlotKwargs],
) -> None:
    opts = get_figure_settings(**kwargs)
    fig, ax = plt.subplots(1, 1, dpi=opts.dpi, figsize=opts.figsize, layout=opts.layout)
    update_figure_setting(fig, **kwargs)
    styles = get_figure_styles(**kwargs)
    for x, y in data:
        ax.semilogx(x, y / scale, **styles)
    if ylim:
        ax.set_ylim(ylim)
    if fout:
        fig.savefig(fout, transparent=opts.transparency)
    else:
        plt.show()
    plt.close(fig)
