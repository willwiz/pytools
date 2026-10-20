import timeit
from typing import TYPE_CHECKING

import numpy as np

from pytools.logging import get_logger
from pytools.math._umath import optimized_add_at

if TYPE_CHECKING:
    from pytools.arrays import Arr

_SYSTEM_RAM_LIMIT_GB = 10


def np_add_at(
    indicies: Arr[..., np.integer], values: Arr[..., np.floating]
) -> Arr[..., np.floating]:
    result = np.zeros((indicies.max() + 1, values.shape[-1]), dtype=values.dtype)
    np.add.at(result, indicies.ravel(), values.reshape(-1, values.shape[-1]))
    return result


def np_add_at_opt(
    indicies: Arr[..., np.integer], values: Arr[..., np.floating]
) -> Arr[..., np.floating]:
    result = np.zeros((values.shape[-1], indicies.max() + 1), dtype=values.dtype)
    for i in range(values.shape[-1]):
        np.add.at(result[i], indicies.ravel(), values[..., i].ravel())
    return result.T


def benchmark(nnodes: int, nelem: int, elem: int, dim: int) -> None:
    if nnodes < nelem:
        return
    log = get_logger()
    input_memory_gb = ((nelem * elem * dim * 8) + (nelem * elem * 8)) / 1e9

    # 28GB System Safety Budget: Skip loops demanding more than ~14GB
    # to protect against intermediate runtime accumulation allocations
    if input_memory_gb > _SYSTEM_RAM_LIMIT_GB:
        log.warn(
            f"⚠️ Skipping [nelem={nelem:,} | elem={elem} | dim={dim}] "
            f"-> Requires {input_memory_gb:.1f} GB of raw inputs (Too tight for 28GB system)."
        )
        return
    rng = np.random.default_rng()
    indicies = rng.integers(0, nnodes, size=(nelem, elem))
    values = rng.random(size=(nelem, elem, dim))

    res_numpy = np_add_at(indicies, values)
    res_numpy_columnwise = np_add_at_opt(indicies, values)
    res_optimized = optimized_add_at(indicies, values)

    assert np.allclose(res_numpy, res_optimized)
    assert np.allclose(res_numpy_columnwise, res_optimized)

    time_numpy_columnwise = timeit.timeit(
        "np_add_at_opt(indicies, values)", globals=globals() | locals(), number=10
    )
    time_optimized = timeit.timeit(
        "optimized_add_at(indicies, values)", globals=globals() | locals(), number=10
    )
    log.info(
        f"Benchmark results for nnodes={nnodes}, nelem={nelem}, elem={elem}, dim={dim}:\n"
        f"Numpy add.at (column-wise) time: {time_numpy_columnwise:.6f} seconds\n"
        f"Optimized add_at time: {time_optimized:.6f} seconds\n"
    )


if __name__ == "__main__":
    for nelem in [1e6, 1e7]:
        for nnodes in [1e4, 1e5, 5e5, 1e6]:
            for elem in [3, 9]:
                for dim in [1, 3, 6]:
                    benchmark(int(nnodes), int(nelem), int(elem), int(dim))
