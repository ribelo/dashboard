#-*- coding: utf-8-*-

import numpy as np
from numba.decorators import jit
from numba import double, int8
from server.tool import deepthroat as dt
from server import config


@jit(int8[:](double[:], double[:], double[:], double[:], int8[:], int8[:]))
def get(open, high, low, close, wrb, wrb_hg):
    """Calculate directional creeper movment

    Parameters
    ----------

    Returns
    -------
    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    most_recent_wrb = 0
    last_dcm = 0

    for i in range(size-3):
        # bull dcm
        if wrb_hg[i] == 1:
            # look for most recent bear wrb_hg
            for j in range(1, min(65, i)):
                if wrb_hg[i-j] == -1:
                    most_recent_wrb = i-j
                    break
            else:
                most_recent_wrb = 0
            # check volatiliti contraction
            if (most_recent_wrb and
                close[i] > open[most_recent_wrb] and
                not dt.any(wrb[i+1:i+4]) and
                dt.nanmin(low[i+1:i+4]) > open[i] and
                    dt.nanmin(close[i+1:i+4]) > close[i]):
                    last_dcm = 1
            elif last_dcm == -1:
                last_dcm = 0
        # bear dcm
        if wrb_hg[i] == -1:
            # look for most recent bear wrb_hg
            for j in range(1, min(65, i)):
                if wrb_hg[i-j] == 1:
                    most_recent_wrb = i-j
                    break
            else:
                most_recent_wrb = 0
            # check volatiliti contraction
            if (most_recent_wrb and
                close[i] < open[most_recent_wrb] and
                not dt.any(wrb[i+1:i+4]) and
                dt.nanmax(high[i+1:i+4]) < open[i] and
                    dt.nanmax(close[i+1:i+4]) < close[i]):
                    last_dcm = -1
            elif last_dcm == 1:
                last_dcm = 0

        result[i] = last_dcm

    return result
