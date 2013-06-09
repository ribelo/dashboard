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
    """Array of the bar sizes"""
    cdef:
        double[:] h = df['high']
        double[:] l = df['low']
        np.ndarray[dtype = double, ndim = 1] r = np.empty(h.shape[0], dtype=np.float64)
        Py_ssize_t x

    if lookback == 0:
        lookback = h.shape[0]

    for x in range(lookback):
        if is_nan(h[x]):
            r[x] = NAN_t
            continue
        r[x] = h[x] - l[x]

    return r


