#-*- coding: utf-8-*-

import numpy as np
from numba.decorators import jit
from numba import double, int64, int8


@jit(int8[:](double[:], double[:], int8[:], double[:],
     double[:], int64[:], int8[:], int8[:]))
def basic(open, close, dir, body_size,
          body_mid_point, filled_by, wrb, zones):
    """Calculate fvb confirmation C1/C2

    Parameters
    ----------
    candle open: int64[:]
    candle close: double[:]
    candle dir: int8[:]
    candle body size: double[:]
    candle filled by candle: int64[:]
    candle bars broken by body: int64[:]
    candle wrb: int8[:]

    Returns
    -------
    int8[:]
    bear fvb = -1
    no fvb = 0
    bull fvb = -1
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        if (dir[i] == 1 and wrb[i-1] == -1 and close[i] > body_mid_point[i-1]):
            # Look for zone
            for j in range(2, min(66, i)):  # 64 + 2 = 66
                if (zones[i-j] > 0 and body_size[i-j] > body_size[i-1] and
                    filled_by[i-j] >= i - 1 and
                    ((close[i-1] <= close[i-j] and close[i-1] > open[i-j] and
                     close[i] > close[i-j]) or
                        (close[i-1] < open[i-j] and close[i] >= open[i-j]))):
                    result[i] = 1
        elif (dir[i] == -1 and wrb[i-1] == 1 and close[i] < body_mid_point[i-1]):
            # Look for zone
            for j in range(2, min(66, i)):  # 64 + 2 = 66
                if (zones[i-j] < 0 and body_size[i-j] > body_size[i-1] and
                    filled_by[i-j] >= i - 1 and
                    ((close[i-1] >= close[i-j] and close[i-1] < open[i-j] and
                     close[i] < close[i-j]) or
                        (close[i-1] > open[i-j] and close[i] <= open[i-j]))):
                    result[i] = -1
                    break
    return result
