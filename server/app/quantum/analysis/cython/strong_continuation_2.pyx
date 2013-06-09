#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import numpy as np
cimport numpy as np
import bottleneck as bn
from pkg.quantum.libary._toolbox import *


_DEFAULT = {'lookback': None, 'contraction': 32}


cpdef np.ndarray[dtype = long, ndim = 1] get(df, lookback=None, contraction=32):
    cdef:
        double[:] o = df['open']
        double[:] c = df['close']
        double[:] h = df['high']
        double[:] l = df['low']
        double[:] bs = df['body_size']
        long[:] wrb = df['wrb']
        long[:] wrb_hg = df['wrb_hg']
        long[:] bxc = df['broken_xtrms_by_close']
        long[:] d = df['candle_dir']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(o.shape[0], dtype=np.int64)

        Py_ssize_t v1, v2, x, y, rc, fc

    if not lookback:
        lookback = r.shape[0]

    for v1 in range(4, o.shape[0]):
        # Bullish Strong Continuation
        if wrb_hg[v1] and d[v1] == 1:
            # Must be two white canldes after and above V1
            for x in range(v1 - 1, max(0, v1 - 1 - lookback), -1):
                if l[x] <= o[v1]:
                    break
                if d[x] == 1 and c[x] > c[v1]:
                    rc += 1
                if rc >= 2:
                    break
            if rc < 2:
                rc = 0
                continue
            # Look for V2
            for v2 in range(v1 + 4, v1 + 4 + contraction):
                if (wrb[v2] or wrb_hg[v2]) and d[v2] == 1:
                    rc = 0
                    # V1 must be breakout volatility contraction
                    if v2 - v1 - 1 > bxc[v1]:
                        break
                    # Must be two white canldes before and belove V2
                    for x in range(v1 - 1, max(0, v1 - 1 - lookback), -1):
                        if d[x] == 1 and c[x] < c[v2]:
                            rc += 1
                        if rc >= 2:
                            break
                    if rc < 2:
                        break
                    # Body of V1/V2 must be greater than volatiliti contraction
                    if min(bs[v1], bs[v2]) < bn.nanmax(bs[v1+1:v2]):
                        break
                    # Volatiliti Contraction can't fill V2 and it's prior three
                    # intervals
                    if bn.nanmin(l[v1+1:v2]) <= bn.nanmin(l[v2:v2+3]):
                        break
                    #  Contraction volatiliti must share min 1 pip with V2
                    if bn.nanmin(h[v1+1:v2]) < l[v2] and bn.nanmax(l[v1+1:v2]) > h[v2]:
                        break

                    r[v1] = 1

        # Bearish Strong Continuation
        elif wrb_hg[v1] and d[v1] == -1:
            # Must be two dark canldes after and belove V1
            for x in range(v1 - 1, max(0, v1 - 1 - lookback), -1):
                if h[x] >= o[v1]:
                    break
                if d[x] == -1 and c[x] < c[v1]:
                    fc += 1
                else:
                    fc = 0
                if fc >= 2:
                    break
            if fc < 2:
                fc = 0
                continue
            # Look for V2
            for v2 in range(v1 + 4, v1 + 4 + contraction):
                if (wrb[v2] or wrb_hg[v2]) and d[v2] == -1:
                    fc = 0
                    # V1 must be breakout volatility contraction
                    if v2-v1 > bxc[v1]:
                        break
                    # Must be two dark canldes before and above V2
                    for x in range(v1 - 1, max(0, v1 - 1 - lookback), -1):
                        if d[x] == 1 and c[x] < c[v1]:
                            fc += 1
                        if fc >= 2:
                            break
                    if fc < 2:
                        break
                    # Volatiliti Contraction can't fill V2 and it's prior three
                    # intervals
                    if bn.nanmax(h[v1+1:v2]) >= bn.nanmax(h[v2:v2+3]):
                        break
                    # Body of V1/V2 must be greater than volatiliti contraction
                    if min(bs[v1], bs[v2]) < bn.nanmax(bs[v1+1:v2]):
                        break
                    #  Contraction volatiliti must share min 1 pip with V2
                    if bn.nanmax(l[v1+1:v2]) > h[v2] and bn.nanmin(h[v1+1:v2]) < l[v2]:
                        break

                    r[v1] = 1

    return r
