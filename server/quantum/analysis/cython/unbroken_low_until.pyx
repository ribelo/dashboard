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
    cdef:
        double[:] l = df['low']
        np.ndarray[dtype = long, ndim = 1] r = np.empty(l.shape[0], dtype=np.int64)

        Py_ssize_t x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(1, l.shape[0]):
        if is_nan(l[x]):
            r[x] = x
            continue
        for y in range(x - 1, 0, -1):
            if is_nan(l[y]):
                continue
            if l[y] < l[x]:
                r[x] = y
                break
        else:
            r[x] = -1

    return r
