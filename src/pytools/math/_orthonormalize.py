from typing import TYPE_CHECKING, Literal, overload

import numpy as np

if TYPE_CHECKING:
    from pytools.arrays import A1, A2

rng = np.random.default_rng()

_a = rng.random((100, 3))
_b = rng.random((100, 3))
_PROJECTION_PATH = np.einsum_path("ij,ij,ik", _b, _a, _a)


@overload
def orthonormal_basis[F: np.floating](a: A1[F], b: A1[F], *, flatten: Literal[True]) -> A2[F]: ...
@overload
def orthonormal_basis[F: np.floating](a: A1[F], b: A1[F], *, flatten: Literal[False]) -> A1[F]: ...
def orthonormal_basis[F: np.floating](a: A1[F], b: A1[F], *, flatten: bool = False):
    r"""Orthonormalize two vectors a and b using the Gram-Schmidt process.

    Parameters
    ----------
    a: np.ndarray[tuple[int], F] | np.ndarray[tuple[int, int], F]
        First vector of floating type F
    b: np.ndarray[tuple[int], F] | np.ndarray[tuple[int, int], F]
        Second vector of floating type F

    Returns
    -------
    np.ndarray[tuple[int, int], F]
        Matrix of row basis vectors. Row 1 (index 0) is always a/||a||_2, and row 2 (index 1) is the
        orthonormalized version of b.

    Raises
    ------
    None

    """
    dtype = a.dtype
    a = (a / np.sqrt(np.einsum("ij,ij->i", a, a))).astype(dtype)
    b = (b - np.einsum("ij,ij,ik->ik", b, a, a, optimize=_PROJECTION_PATH)).astype(dtype)
    b = (b / np.sqrt(np.einsum("ij,ij->i", b, b))).astype(dtype)
    c = np.cross(a, b)
    c = (c / np.sqrt(np.einsum("ij,ij->i", c, c))).astype(dtype)
    res = np.hstack((a, b, c)) if flatten else np.transpose(np.dstack((a, b, c)), (0, 2, 1))
    return np.ascontiguousarray(res).astype(dtype)
