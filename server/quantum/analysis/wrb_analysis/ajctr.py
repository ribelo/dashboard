#-*- coding: utf-8-*-

from numba import double, int64
from numba.decorators import jit
import numpy as np
import tool.deepthroat as dt


@jit(double[:](double[:], double[:], double[:], int64[:],
               double[:], double[:], double[:s]))
def _hammer_line(open, high, low, close, dir,
                 body_size, shadow_upper, shadow_lower):
    """Calculate candle hammer line

    Parameters
    ----------
    candle open: double
    candle high: double
    candle low: double
    candle close: double
    candle dir: int64
    candle body_size: double
    candle shadow_upper: double
    candle shadow_lower: double

    Returns
    -------
    int64

    bear hammer line = -1
    no hammer line = 0
    bull hammer line = 1
    """
    # bull hammer
    if (dir == 1 and body_size > shadow_upper and
        shadow_lower > body_size + shadow_upper and
            shadow_lower > shadow_upper):
        return 1
    # bear hammer
    elif (dir == -1 and body_size > shadow_lower and
          shadow_upper > body_size + shadow_lower and
            shadow_upper > shadow_lower):
        return -1
    else:
        return 0


def hammer(open, high, low, close, wrb):
    """Calculate candle hammer

    Parameters
    ----------
    candle open: double[:]
    candle high: double[:]
    candle low: double[:]
    candle close: double[:]

    Returns
    -------
    int64

    bear hammer = -1
    no hammer = 0
    bull hammer = 1
    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        # look for wrb
        found_wrb = False
        for j in range(3):
            if wrb[i-j]:
                fount_wrb = True
                break
        if (found_wrb and low[i] < dt.nanmin(low[i-j-3:i]) and
            shadow_lower[i] > shadow_lower[i-j-3:i] and
                shadow_lower[i] > body_size[i-j-3:i]):
            for j in range(3):
                if dir[i-j] == -1:




            not found_wrb and low[i] < dt.nanmin(low[i-3:i]) and
            shadow_lower[i] > shadow_lower[i-3:i] and
            shadow_lower[i] > body_size[i-3]):
