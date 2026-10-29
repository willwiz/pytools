from typing import Literal, overload

import numpy as np

from pytools.arrays import A1, A2

@overload
def orthonormal_basis[F: np.floating](a: A1[F], b: A1[F], *, flatten: Literal[True]) -> A2[F]: ...
@overload
def orthonormal_basis[F: np.floating](a: A1[F], b: A1[F], *, flatten: Literal[False]) -> A1[F]: ...
