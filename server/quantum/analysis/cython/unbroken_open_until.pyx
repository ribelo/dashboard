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
        double[:] o = df['open']
        double[:] h = df['high']
        double[:] l = df['low']
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(o.shape[0], dtype=np.int64)

        Py_ssize_t x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(o.shape[0]):
        if is_nan(o[x]):
            r[x] = 0
            continue

        if cd[x] == 1:
            for y in range(x - 1, 0, -1):
                if is_nan(o[y]):
                    continue
                if l[y] < o[x]:
                    r[x] = y
                    break
            else:
                r[x] = -1

        elif cd[x] == -1:
            for y in range(x - 1, 0, -1):
                if is_nan(o[y]):
                    continue
                if h[y] > o[x]:
                    r[x] = y
                    break
            else:
                r[x] = -1

    return r
