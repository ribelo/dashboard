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
        double[:] c = df['close']
        double[:] h = df['high']
        double[:] l = df['low']
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] rh = df['reaction_high']
        np.ndarray[dtype = long, ndim = 1] rl = df['reaction_low']
        np.ndarray[dtype = long, ndim = 1] r = np.empty(o.shape[0], dtype=np.int64)

        Py_ssize_t x, y,

    if not lookback:
        lookback = r.shape[0]

    for x in range(o.shape[0]):
        if is_nan(o[x]):
            r[x] = -1
            continue
        if rh[x]:
            for y in range(x + 1, x + lookback):
                if is_nan(o[x]) or cd[y] != 1:
                    continue
                if r[y] > 0 or rh[y]:
                    break
                if o[y] < h[x] and c[y] > h[x]:
                    r[y] = x
                elif h[y] > h[x]:
                    r[y] = -1
                    break
        elif rl[x]:
            for y in range(x + 1, x + lookback):
                if is_nan(o[x]) or cd[y] != -1:
                    continue
                if r[y] > 0 or rl[y]:
                    break
                if o[y] > l[x] and c[y] < l[x]:
                    r[y] = x
                elif l[y] < l[x]:
                    r[y] = -1
                    break

    return r
