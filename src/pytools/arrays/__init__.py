from __future__ import annotations

import numpy as np

__all__ = [
    "A1",
    "A2",
    "A3",
    "S1D",
    "S2D",
    "S3D",
    "T1",
    "T2",
    "T3",
    "Arr",
    "SAny",
]


type SAny = tuple[int, ...]
type S1D = tuple[int]
type S2D = tuple[int, int]
type S3D = tuple[int, int, int]

type Arr[S: tuple[int, ...], T: np.generic] = np.ndarray[S, np.dtype[T]]
type A1[T: np.generic] = np.ndarray[tuple[int], np.dtype[T]]
type A2[T: np.generic] = np.ndarray[tuple[int, int], np.dtype[T]]
type A3[T: np.generic] = np.ndarray[tuple[int, int, int], np.dtype[T]]

type T1[T: (float, int)] = tuple[T]
type T2[T: (float, int)] = tuple[T, T]
type T3[T: (float, int)] = tuple[T, T, T]
