#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np
from pkg.quantum.libary._toolbox import *


_DEFAULT = {'lookback': None}

cpdef double FPINF_t = np.PINF
cpdef double FNINF_t = np.NINF
cpdef long IPINF_t = np.iinfo(np.int64).max
cpdef long ININF_t = np.iinfo(np.int64).min
cpdef object NAN_t = np.NaN

cpdef char is_nan(double a):
    return a != a
cpdef char is_finf(double a):
    return a == FPINF_t or a == FNINF_t
cpdef char is_iinf(long a):
    return a == IPINF_t or a == ININF_t

cpdef np.ndarray[dtype = long, ndim = 1] get(df, lookback=None):
    cdef:
        double[:] h = df['high']
        long[:] cd = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(h.shape[0], dtype=np.int64)

        double rh = FNINF_t

        Py_ssize_t x, y, cr, cf

    if not lookback:
        lookback = r.shape[0]

    for x in range(3, lookback - 3):
        if is_nan(h[x]):
            continue
        rh = h[x]
        cr = 0
        cf = 0
        for y in range(1, 65):
            if x - y < 0 or x + y >= lookback:
                break
            if is_nan(h[y]):
                continue
            if cr >= 2 and cf >= 2:
                r[x] = True
                break
            if h[x + y] > rh or h[x - y] > rh:
                rh = FNINF_t
                cr = 0
                cr = 0
                break
            if cr < 2:
                if cd[x + y] == 1:
                    cr += 1
                else:
                    cr = 0
            if cf < 2:
                if cd[x - y] == -1:
                    cf += 1
                else:
                    cf = 0

    return r
