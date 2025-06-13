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


from .api import close_figure, create_figure
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
