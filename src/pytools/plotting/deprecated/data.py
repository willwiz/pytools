from __future__ import annotations

__all__ = ["LEGEND_KWARGS", "FigureSettings", "PlotCyclers", "PlotKwargs", "PlotStyles"]
import dataclasses as dc
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from collections.abc import Sequence


@dc.dataclass(slots=True)
class PlotCyclers:
    color: Sequence[str] | None = None
    mec: Sequence[str] | None = None
    alpha: Sequence[float] | None = None
    linestyle: Sequence[str] | None = None
    linewidth: Sequence[float] | None = None
    marker: Sequence[str] | None = None


class PlotStyles(TypedDict, total=False):
    markersize: int | float
    markevery: int | Sequence[int] | float | Sequence[float] | None
    fillstyle: str
    markeredgewidth: float


@dc.dataclass(slots=True, kw_only=True)
class FigureSettings:
    figsize: tuple[int, int] = (4, 3)
    dpi: int = 180
    layout: Literal["constrained"] = "constrained"
    transparency: bool = False
