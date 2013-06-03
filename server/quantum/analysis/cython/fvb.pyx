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
        double[:] bmp = df['body_mid_point']
        long[:] uou = df['unbroken_open_until']
        long[:] d = df['candle_dir']
        long[:] wrb = df['wrb']

        long[:] sp1 = df['swing_point_1']
        long[:] sp2 = df['swing_point_2']
        long[:] sc1 = df['strong_continuation_1']
        long[:] sc2 = df['strong_continuation_2']
        long[:] sc3 = df['strong_continuation_3']
        long[:] sc4 = df['strong_continuation_4']

        np.ndarray[dtype = long, ndim = 1] r = np.empty(o.shape[0], dtype=np.int64)

        Py_ssize_t x, y

    if not lookback:
        lookback = r.shape[0]

    for x in range(o.shape[0]):
        r[x] = -1
        # C2 must be wrb
        if wrb[x+1]:
            # bull
            if d[x+1] == -1 and d[x] == 1 and c[x] > bmp[x+1]:
                # Look for zone
                for y in range(x + 2, min(o.shape[0], x + 2 + lookback)):
                    if d[y] == 1 and (sp1[y] or sp2[y] or sc1[y] or sc2[y] or sc3[y] or sc4[y]):
                        if bs[x+1] >= bs[y]:
                            continue
                        if uou[y] < x - 1:
                            continue
                        if (c[x+1] < c[y] and c[x] > c[y]) or (c[x+1] < o[y] and c[x] > o[y]):
                            r[x] = True
                            break
            # bear
            elif d[x+1] == 1 and d[x] == -1 and c[x] < bmp[x+1]:
                # Look for zone
                for y in range(x + 2, min(o.shape[0], x + 2 + lookback)):
                    if d[y] == -1 and (sp1[y] or sp2[y] or sc1[y] or sc2[y] or sc3[y] or sc4[y]):
                        if bs[x+1] >= bs[y]:
                            continue
                        if uou[y] < x - 1:
                            continue
                        if (c[x+1] > c[y] and c[x] < c[y]) or (c[x+1] > o[y] and c[x] < o[y]):
                            r[x] = True
                            break

    return r
