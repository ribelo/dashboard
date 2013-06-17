#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np
from pkg.quantum.libary._toolbox import *


_DEFAULT = {'lookback': None}


cpdef np.ndarray[dtype = double, ndim = 1]  get(df, lookback=None):
    """Array of the up shadow sizes"""
    cdef:
        double[:] o = df['open']
        double[:] c = df['close']
        double[:] h = df['high']
        np.ndarray[dtype = double, ndim = 1] r = np.empty(o.shape[0], dtype=np.float64)

        Py_ssize_t x

    if not lookback:
        lookback = r.shape[0]

    for x in range(o.shape[0]):
        if is_nan(o[x]):
            r[x] = NAN_t
            continue
        r[x] = h[x] - max(c[x], o[x])

    return r