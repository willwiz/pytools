from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pytools.arrays import A2, Arr, SAny


def optimized_add_at[F: np.floating](index: Arr[SAny, np.integer], weights: Arr[SAny, F]) -> A2[F]:
    """Optimized version of np.add.at for 1D arrays.

    index [..., I] * weights [..., I, J] -> [..., I, J]

    Type Parameters
    ---------------
    F : np.floating

    Parameters
    ----------
    index : Arr[SAny, np.integer]
        The row indices where the weights will be added. Contains integer in [0, N). Size of index
        is [..., I].
    weights : Arr[SAny, F]
        The weights to be added. Size of weights is [..., I, J].

    Returns
    -------
    A1[F]
        The resulting array after adding the weights at the specified indices. Size [..., I, J]

    """
    size = int(index.max() + 1)
    unraveled_index = index.ravel()
    result = np.zeros((size, weights.shape[-1]), dtype=weights.dtype)
    for i in range(weights.shape[-1]):
        result[:, i] = np.bincount(unraveled_index, weights=weights[..., i].ravel(), minlength=size)
    return result
