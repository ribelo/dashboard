#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np

_DEFAULT = {'lookback': None}

cdef inline char is_nan(double a) nogil:
    return a != a

cpdef np.ndarray[dtype = long, ndim = 1] get(df, lookback=None):
    """Quantity array of broken body sizes"""
    cdef:
        double[:] bs = df['body_size']
        np.ndarray[dtype = long, ndim = 1] r = np.empty(bs.shape[0], dtype=np.int64)
        Py_ssize_t x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(lookback):
        if is_nan(bs[x]):
            r[x] = 0
            continue
        for y in range(x + 1, lookback):
            if is_nan(bs[y]):
                continue
            if bs[x] > bs[y]:
                continue
            else:
                r[x] = y - x - 1
                break
        else:
            r[x] = x

    return r
