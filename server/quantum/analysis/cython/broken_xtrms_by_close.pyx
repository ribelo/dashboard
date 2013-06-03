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

    """Quantity array of broken extremes by close"""
    cdef:
        double[:] c = df['close']
        double[:] h = df['high']
        double[:] l = df['low']
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(c.shape[0], dtype=np.int64)

        Py_ssize_t x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(c.shape[0]):
        if is_nan(c[x]):
            r[x] = 0
            continue
        if cd[x] == 1:
            for y in range(x + 1, c.shape[0]):
                if is_nan(c[y]):
                    continue
                if c[x] > h[y]:
                    continue
                else:
                    r[x] = y - x - 1
                    break
            else:
                r[x] = x
        elif cd[x] == -1:
            for y in range(x + 1, c.shape[0]):
                if is_nan(c[y]):
                    continue
                if c[x] < l[y]:
                    continue
                else:
                    r[x] = y - x - 1
                    break
            else:
                r[x] = x

    return r
