from typing import TYPE_CHECKING

import numpy as np
from numpy import linalg

if TYPE_CHECKING:
    from pytools.arrays import A1, A2


def householder_orthogonal_basis[F: np.floating](v: A1[F]) -> A2[F]:
    r"""Find the complete 3D orthogonal basis of with v using householder projection.

    let u_1 = v/||v||_2 be one basis vector of the set.
    the set of basis row vectors, H = [u_1; u_2; u_3; ...], where:
            u_i \cdot u_j == 0 for all i =/= j
            u_i \cdot u_j == \pm 1 for i ==j
    is given by:
        H = I - 2 * u_1^T \otimes u_1 / (u_1 \cdot u_1)

    Parameters
    ----------
    v: np.ndarray[tuple[int], F]
        Any vector of floating type F

    Returns
    -------
    np.ndarray[tuple[int, int], F]
        Matrix of row basis vectors. Row 1 (index 0) is always v/||v||_2

    Raises
    ------
    None

    """
    dtype = v.dtype
    v = (v / linalg.norm(v).astype(dtype)).astype(dtype)
    w = (v - np.array([1, 0, 0], dtype=dtype)).astype(dtype)
    h = (np.eye(len(v), dtype=dtype) - 2 * np.outer(w, w) / np.dot(w, w)).astype(dtype)
    j = linalg.det(h)
    if j < 0:
        h[2, :] = -h[2, :]
    return h
