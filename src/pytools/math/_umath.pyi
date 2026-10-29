import numpy as np

from pytools.arrays import A2, Arr, SAny

def optimized_add_at[F: np.floating](
    index: Arr[SAny, np.integer], weights: Arr[SAny, F]
) -> A2[F]: ...
