from typing import Literal, overload

import numpy as np

from pytools.arrays import A1, A2, A3
from pytools.result import Result

@overload
def r_basis[F: np.floating](v: A1[F], *, flatten: Literal[True]) -> Result[A1[F]]: ...
@overload
def r_basis[F: np.floating](v: A1[F], *, flatten: Literal[False]) -> Result[A2[F]]: ...
@overload
def r_basis[F: np.floating](v: A2[F], *, flatten: Literal[True]) -> Result[A2[F]]: ...
@overload
def r_basis[F: np.floating](v: A2[F], *, flatten: Literal[False]) -> Result[A3[F]]: ...
