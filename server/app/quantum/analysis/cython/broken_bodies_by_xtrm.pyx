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
    """Quantity array of broken bodies"""
    cdef:
        double[:] o = df['open']
        double[:] c = df['close']
        double[:] h = df['high']
        double[:] l = df['low']
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] r = np.empty(o.shape[0], dtype=np.int64)

        Py_ssize_t x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(o.shape[0]):
        if is_nan(o[x]):
            r[x] = 0
            continue
        if cd[x] == 1:
            for y in range(x + 1, o.shape[0]):
                if is_nan(o[y]):
                    continue
                if h[x] > h[y]:
                    continue
                elif h[x] > max(c[y], o[y]):
                    r[x] = y - x - 1
                    break
            else:
                r[x] = x
        elif cd[x] == -1:
            for y in range(x + 1, o.shape[0]):
                if is_nan(o[y]):
                    continue
                if l[x] < l[y]:
                    continue
                elif l[x] < min(c[y], o[y]):
                    r[x] = y - x - 1
                    break
            else:
                r[x] = x

    return r


