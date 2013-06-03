#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np
from pkg.quantum.libary._toolbox import *


_DEFAULT = {'lookback': None}


cpdef np.ndarray[dtype = long, ndim = 1] get(df, lookback=None):
    """Quantity array of broken bar sizes"""
    cdef:
        double[:] bs = df['bar_size']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(bs.shape[0], dtype=np.int64)

        Py_ssize_t cc, x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(lookback):
        if is_nan(bs[x]):
            r[x] = 0
            continue
        for y in range(x + 1, bs.shape[0]):
            if is_nan(bs[y]):
                continue
            if bs[x] > bs[y]:
                continue
            else:
                r[x] = y - x - 1
                break
        else:
            r[x] = x

    return r


