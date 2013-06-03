#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np
from pkg.quantum.libary._toolbox import *


_DEFAULT = {'lookback': None}


cpdef np.ndarray[dtype = long, ndim = 1] get(df, lookback=None, wrb_size=3):
    cdef:
        long[:] bbs = df['broken_bodies_size']
        long[:] bxc = df['broken_xtrms_by_close']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(bbs.shape[0], dtype=np.int64)
        Py_ssize_t x

    if not lookback:
        lookback = r.shape[0]

    for x in range(bbs.shape[0]):
        if bbs[x] >= wrb_size and bxc[x] >= wrb_size:
            r[x] = 1

    return r
