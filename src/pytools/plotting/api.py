# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

__all__ = [
    "close_figure",
    "create_figure",
]

from typing import TYPE_CHECKING, Any, Literal, Unpack

from matplotlib import pyplot as plt

from .impl import figure_kwargs

if TYPE_CHECKING:
    import numpy as np
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from .typing import (
        PlotKwargs,
    )


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
    dims: dict[Literal["ncols", "nrows"], int] = {
        "ncols": ncols if ncols is not None else 1,
        "nrows": nrows if nrows is not None else 1,
    }
    fig, ax = plt.subplots(**dims, squeeze=False, **opts)
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
