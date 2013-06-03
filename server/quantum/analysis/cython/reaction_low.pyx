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
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(l.shape[0], dtype=np.int64)

        double rl = FPINF_t

        Py_ssize_t x, y, cr, cf

    if not lookback:
        lookback = r.shape[0]

    for x in range(l.shape[0]):
        if is_nan(l[x]):
            continue
        rl = l[x]
        cr = 0
        cf = 0
        for y in range(1, min(lookback, l.shape[0] - x)):
            if is_nan(l[y]):
                continue
            if cr >= 2 and cf >= 2:
                break
            if l[x + y] < rl or l[x - y] < rl:
                rl = FPINF_t
                cr = 0
                cr = 0
                break
            if cf < 2:
                if cd[x + y] == -1:
                    cf += 1
                else:
                    cf = 0
            if cr < 2:
                if cd[x - y] == 1:
                    cr += 1
                else:
                    cr = 0

        if cf == 2 and cr == 2:
            r[x] = True
            continue

    return r
