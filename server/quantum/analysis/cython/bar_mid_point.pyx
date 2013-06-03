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
    """Array of the candle body sizes"""
    cdef:
        double[:] h = df['high']
        double[:] l = df['low']
        np.ndarray[dtype = double, ndim = 1] r = np.empty(o.shape[0], dtype=np.float64)
        Py_ssize_t x

    if not lookback:
        lookback = r.shape[0]

    for x in range(lookback):
        if is_nan(o[x]):
            r[x] = NAN_t
            continue
        r[x] = (h[x] + l[x]) * .5

    return r
