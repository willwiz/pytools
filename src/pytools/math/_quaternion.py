from typing import TYPE_CHECKING, Literal, overload

import numpy as np
from scipy.spatial.transform import Rotation

from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from pytools.arrays import A1, A2, A3

e1 = np.array([1, 0, 0], np.float64)


@overload
def _r_basis[F: np.floating](v: A1[F], *, flatten: Literal[True]) -> A1[F]: ...
@overload
def _r_basis[F: np.floating](v: A1[F], *, flatten: Literal[False]) -> A2[F]: ...
def _r_basis[F: np.floating](v: A1[F], *, flatten: bool) -> A1[F] | A2[F]:
    rot, _ = Rotation.align_vectors(e1, v)
    r = rot.as_matrix().astype(v.dtype).T
    if flatten:
        r = r.flatten()
    return rot.as_matrix().astype(v.dtype).T


def r_basis[F: np.floating](
    v: NDArray[F], *, flatten: bool = False
) -> Result[A1[F] | A2[F] | A3[F]]:
    """Return orthonormal basis from given vectors."""
    match v.shape:
        case (3,):
            return Ok(_r_basis(v, flatten=flatten))
        case (_, 3): ...  # fmt: skip
        case _:
            msg = "only 3D vector or array of vectors allowed."
            return Err(ValueError(msg))
    return Ok(np.ascontiguousarray([_r_basis(vi, flatten=flatten) for vi in v], dtype=v.dtype))
