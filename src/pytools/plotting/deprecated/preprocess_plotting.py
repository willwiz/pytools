# pyright: reportUnknownMemberType=false
import matplotlib.pyplot as plt
from arraystubs import Mat, dbl

from trabeculae.data_types import TrabeculaeMetrics


def plot_breaks(data: Mat[dbl], metrics: TrabeculaeMetrics, fout: str) -> None:
    figure = plt.figure(figsize=(12, 3), dpi=300)
    plt.plot(data[:, 0], data[:, 1], "-", markersize=1, color="black", label="Data")
    plt.plot(
        data[metrics["index"], 0],
        data[metrics["index"], 1],
        "o",
        markersize=3,
        markeredgewidth=0.2,
        fillstyle="none",
        color="red",
        label="Breaks",
    )
    for i in metrics["index"]:
        plt.annotate(str(i), (data[i, 0], data[i, 1]), fontsize=3, color="red")
    plt.savefig(fout)
    plt.close(figure)


def plot_forces(data: Mat[dbl], metrics: TrabeculaeMetrics, fout: str) -> None:
    figure = plt.figure(figsize=(12, 3), dpi=300)
    plt.plot(data[:, 0], data[:, 2], "-", markersize=1, color="black", label="Data")
    plt.plot(
        data[metrics["index"], 0],
        data[metrics["index"], 2],
        "o",
        markersize=3,
        markeredgewidth=0.2,
        fillstyle="none",
        color="red",
        label="Forces",
    )
    plt.savefig(fout)
    plt.close(figure)
