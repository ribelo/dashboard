#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np
from pkg.quantum.libary._toolbox import *


_DEFAULT = {'lookback': None}

cdef inline char is_nan(double a) nogil:
    return a != a
cpdef object NAN_t = np.NaN
cpdef np.ndarray[dtype = double, ndim = 1]  get(df, lookback=None):
    """Array of the gap sizes"""
    cdef:
        double[:] h = df['high']
        double[:] l = df['low']
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = double, ndim = 1] r = np.empty(h.shape[0], dtype=np.float64)

        Py_ssize_t x

    if not lookback:
        lookback = r.shape[0]

    r[0] = NAN_t
    r[h.shape[0] - 1] = NAN_t

    for x in range(1, h.shape[0] - 1):
        if is_nan(h[x]):
            r[x] = NAN_t
            continue
        if cd[x] == 1:
            r[x] = h[x - 1] - l[x + 1]
        else:
            r[x] = l[x + 1] - h[x - 1]

    return r
