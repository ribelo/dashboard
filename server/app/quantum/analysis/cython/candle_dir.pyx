#-*- coding: utf-8-*-
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: embedsignature=True

import os
import json
import numpy as np
cimport numpy as np
from pkg.quantum.libary._toolbox import *

_CONFIG_PATH = os.path.join('app.config', 'indicator.json')
_NAME = 'candle_dir'
_DEFAULT = {'lookback': None}
_app.config = json.load(open(_CONFIG_PATH)).get(_NAME)



cpdef np.ndarray[dtype = long, ndim = 1] get(df, lookback=None):
    """Array of the direction of the candles, with 1 bull, 0 equals -1 bear"""
    cdef:
        double[:] o = df['open']
        double[:] c = df['close']
        np.ndarray[dtype = long, ndim = 1] r = np.zeros(o.shape[0], dtype=np.int64)
        Py_ssize_t x

    if not lookback:
        lookback = r.shape[0]

    for x in range(lookback):
        if c[x] > o[x]:
            r[x] = 1
        elif c[x] < o[x]:
            r[x] = -1

    return r
