#-*- coding: utf-8-*-

import numpy as np
from numba.decorators import jit
from numba import double, int64, int8
from app.config import QUANTUM_LOOK_BACK


@jit(int8[:](double[:], double[:], int8[:], double[:], int64[:], int8[:], int8[:],
     double[:], double[:], int8[:], double[:], int64[:], int8[:], int8[:]))
def vtr(open1, close1, dir1, body_mid_point1, filled_by1, wrb_hg1, zones1,
        open2, close2, dir2, body_mid_point2, filled_by2, wrb_hg2, zones2):
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

    size = open1.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        if ((dir1[i] == 1 and dir2[i] == 1 and dir1[i - 1] == -1 and
            close1[i] > body_mid_point1[i - 1]) or
            (dir2[i] == 1 and dir1[i] == 1 and dir2[i - 1] == -1 and
                close2[i] > body_mid_point2[i - 1])):
             # Look for zone
            for j in range(2, min(QUANTUM_LOOK_BACK + 2, i)):
                if ((zones1[i - j] > 0 and wrb_hg2[i - j] == 1 and
                    filled_by1[i - j] >= i) or
                    (zones2[i - j] > 0 and wrb_hg1[i - j] == 1 and
                        filled_by2[i - j] >= i)):
                    if (close1[i - 1] <= close1[i - j] and
                        close1[i - 1] > open1[i - j] and
                            close1[i] > close1[i - j]):
                        if (close2[i - 1] < open2[i - j] or
                                close2[i - 1] > close2[i - j]):
                            result[i] = 1
                            break
        elif ((dir1[i] == -1 and dir2[i] == -1 and dir1[i - 1] == 1 and
               close1[i] > body_mid_point1[i - 1]) or
             (dir2[i] == -1 and dir1[i] == -1 and dir2[i - 1] == 1 and
                close2[i] < body_mid_point2[i - 1])):
            # Look for zone
            for j in range(2, min(QUANTUM_LOOK_BACK + 2, i)):
                if ((zones1[i - j] < 0 and wrb_hg2[i - j] == -1 and
                   filled_by1[i - j] >= i) or
                   (zones2[i - j] < 0 and wrb_hg1[i - j] == -1 and
                   filled_by2[i - j] >= i)):
                    if (close1[i - 1] >= close1[i - j] and
                        close1[i - 1] < open1[i - j] and
                            close1[i] < close1[i - j]):
                        if (close2[i - 1] < close2[i - j] or
                                close2[i - 1] > open2[i - j]):
                            result[i] = -1
                            break

    return result
