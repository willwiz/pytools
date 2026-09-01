from typing import TYPE_CHECKING

import numpy as np
from scipy.spatial.transform import Rotation

from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from pytools.arrays import A1, A2, A3

e1 = np.array([1, 0, 0], np.float64)


def _r_basis[F: np.floating](v: A1[F]) -> A2[F]:
    rot, _ = Rotation.align_vectors(e1, v)
    return rot.as_matrix().astype(v.dtype).T


def r_basis[F: np.floating](v: NDArray[F]) -> Result[A2[F]] | Result[A3[F]]:
    """Return orthonormal basis from given vectors."""
    match v.shape:
        case (3,):
            return Ok(_r_basis(v))
        case (_, 3): ...  # fmt: skip
        case _:
            msg = "only 3D vector or array of vectors allowed."
            return Err(ValueError(msg))
    return Ok(np.ascontiguousarray([_r_basis(vi) for vi in v], dtype=v.dtype))
