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
        long[:] wrb = df['wrb']
        double[:] g = df['gap']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(wrb.shape[0], dtype=np.int64)
        Py_ssize_t x

    if not lookback:
        lookback = r.shape[0]

    for x in range(wrb.shape[0]):
        if wrb[x] and g[x] > 0:
            r[x] = 1

    return r
