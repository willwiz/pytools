from typing import Literal, overload

import numpy as np
from numpy.typing import NDArray

from pytools.arrays import A1, A2, A3
from pytools.result import Result

@overload
def _r_basis[F: np.floating](v: A1[F], *, flatten: Literal[True]) -> A1[F]: ...
@overload
def _r_basis[F: np.floating](v: A1[F], *, flatten: Literal[False]) -> A2[F]: ...
def r_basis[F: np.floating](
    v: NDArray[F], *, flatten: bool = False
) -> Result[A1[F] | A2[F] | A3[F]]: ...
