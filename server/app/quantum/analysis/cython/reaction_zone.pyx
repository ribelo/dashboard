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
        double[:] bs = df['body_size']
        long[:] wrb_hg = df['wrb_hg']
        long[:] d = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] rh = df['reaction_high']
        np.ndarray[dtype = long, ndim = 1] rl = df['reaction_low']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(o.shape[0], dtype=np.int64)

        Py_ssize_t v1, v2, x, y
        double hh, ll

    if not lookback:
        lookback = r.shape[0]

    for v1 in range(4, o.shape[0]):
        hh = FNINF_t
        ll = FPINF_t
        # Bullish Strong Continuation
        if wrb_hg[v1] and d[v1] == 1:
            # Look for reaction low
            for x in range(v1 - 1, max(0, v1 - 1 - lookback), -1):
                ll = min(ll, l[x])
                if l[x] > c[v1]:
                    continue
                if l[x] > ll:
                    continue
                if l[x] < o[v1]:
                    break
                if not rl[x]:
                    continue

                r[v1] = 1

        # Bearish Strong Continuation
        elif wrb_hg[v1] and d[v1] == -1:
            # Look for reaction high
            for x in range(v1 - 1, max(0, v1 - 1 - lookback), -1):
                hh = max(hh, h[x])
                if h[x] > c[v1]:
                    continue
                if h[x] > hh:
                    continue
                if h[x] < o[v1]:
                    break
                if not rh[x]:
                    continue

                r[v1] = 1

    return r
