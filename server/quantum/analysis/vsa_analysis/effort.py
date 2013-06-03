#-*- coding: utf-8-*-
import numpy as np
from numba.decorators import jit
from numba import double, int8


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], double[:], int8[:]))
def eff1(open, high, low, close, volume,
         volume_average, bar_size, bar_mid_point, wrb):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        # effort to rise / bull
        if (high[i] > high[i-1] and low[i] >= low[i-1] and
            bar_size[i] == bar_size[i-1] and
            open[i] <= low[i] + (high[i] - low[i])*.1 and
            close[i] >= low[i] + (high[i] - low[i])*.9 and
            close[i] > close[i-1] and bar_mid_point[i] > high[i-1] and
            volume[i] > volume[i-1] and volume[i] > volume_average[i] and
                volume[i] <= 2*volume_average[i] and wrb[i] == 1):
            result[i] = 1
        # effort to fall / bear
        elif (low[i] < low[i-1] and high[i] <= high[i-1] and
              bar_size[i] == bar_size[i-1] and
              open[i] >= low[i] + (high[i] - low[i])*.9 and
              close[i] <= low[i] + (high[i] - low[i])*.1 and
              close[i] < close[i-1] and bar_mid_point[i] < low[i-1] and
              volume[i] > volume[i-1] and volume[i] > volume_average[i] and
                volume[i] <= 2*volume_average[i] and wrb[i] == -1):
            result[i] = -1
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], double[:], int8[:]))
def eff2(open, high, low, close, volume,
         volume_average, bar_size, bar_mid_point, wrb):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        # effort to rise / bull
        if (high[i] > high[i-1] and low[i] >= low[i-1] and
            bar_size[i] > bar_size[i-1] and
            open[i] <= low[i] + (high[i] - low[i])*.2 and
            close[i] >= low[i] + (high[i] - low[i])*.8 and
            close[i] > close[i-1] and bar_mid_point[i] >= high[i-1] and
            volume[i] > volume[i-1] and volume[i] > 2*volume_average[i] and
            volume[i] <= 4*volume_average[i] and
                wrb[i] == 1 and close[i] < close[i+1]):
            result[i] = 1
        # effort to fall / bear
        elif (low[i] < low[i-1] and high[i] <= high[i-1] and
              bar_size[i] > bar_size[i-1] and
              open[i] >= low[i] + (high[i] - low[i])*.8 and
              close[i] <= low[i] + (high[i] - low[i])*.2 and
              close[i] < close[i-1] and bar_mid_point[i] <= low[i-1] and
              volume[i] > volume[i-1] and volume[i] > 2*volume_average[i] and
              volume[i] <= 4*volume_average[i] and
                wrb[i] == -1 and close[i] > close[i+1]):
            result[i] = -1
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], double[:], int8[:]))
def eff3(open, high, low, close, volume,
         volume_average, bar_size, bar_mid_point, wrb):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        # effort to rise / bull
        if (high[i] > high[i-1] and low[i] >= low[i-1] and
            bar_size[i] == bar_size[i-1] and
            open[i] <= low[i] + (high[i] - low[i])*.1 and
            close[i] >= low[i] + (high[i] - low[i])*.9 and
            close[i] > close[i-1] and bar_mid_point[i] > high[i-1] and
            volume[i] > volume[i-1] and volume[i] > 2*volume_average[i] and
            volume[i] <= 4*volume_average[i] and
                wrb[i] == 1 and close[i] < close[i+1]):
            result[i] = 1
        # effort to fall / bear
        elif (low[i] < low[i-1] and high[i] <= high[i-1] and
              bar_size[i] == bar_size[i-1] and
              open[i] >= low[i] + (high[i] - low[i])*.9 and
              close[i] <= low[i] + (high[i] - low[i])*.1 and
              close[i] < close[i-1] and bar_mid_point[i] < low[i-1] and
              volume[i] > volume[i-1] and volume[i] > 2*volume_average[i] and
              volume[i] <= 4*volume_average[i] and
                wrb[i] == -1 and close[i] > close[i+1]):
            result[i] = -1
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], double[:], int8[:]))
def eff4(open, high, low, close, volume,
         volume_average, bar_size, bar_mid_point, wrb):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        # effort to rise / bull
        if (high[i] > high[i-1] and low[i] >= low[i-1] and
            bar_size[i] > bar_size[i-1] and
            open[i] <= low[i] + (high[i] - low[i])*.2 and
            close[i] >= low[i] + (high[i] - low[i])*.8 and
            close[i] > close[i-1] and bar_mid_point[i] >= high[i-1] and
            volume[i] < volume_average[i] and volume[i] > volume[i-1] and
                volume[i] > volume[i-2] and wrb[i] == 1):
            result[i] = 1
        # effort to fall / bear
        elif (low[i] < low[i-1] and high[i] <= high[i-1] and
              bar_size[i] > bar_size[i-1] and
              open[i] >= low[i] + (high[i] - low[i])*.8 and
              close[i] <= low[i] + (high[i] - low[i])*.2 and
              close[i] < close[i-1] and bar_mid_point[i] <= low[i-1] and
              volume[i] < volume_average[i] and volume[i] > volume[i-1] and
                volume[i] > volume[i-2] and wrb[i] == -1):
            result[i] = -1
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], double[:], int8[:]))
def eff5(open, high, low, close, volume,
         volume_average, bar_size, bar_mid_point, wrb):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        # effort to rise / bull
        if (high[i] > high[i-1] and low[i] >= low[i-1] and
            bar_size[i] == bar_size[i-1] and
            open[i] <= low[i] + (high[i] - low[i])*.1 and
            close[i] >= low[i] + (high[i] - low[i])*.9 and
            close[i] > close[i-1] and bar_mid_point[i] > high[i-1] and
            volume[i] > volume_average[i] and volume[i] > volume[i-1] and
                volume[i-1] > volume[i-2] and wrb[i] == 1):
            result[i] = 1
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] == bar_size[i-1] and
            open[i] >= low[i] + (high[i] - low[i])*.9 and
            close[i] <= low[i] + (high[i] - low[i])*.1 and
            close[i] < close[i-1] and bar_mid_point[i] < low[i-1] and
            volume[i] > volume_average[i] and volume[i] > volume[i-1] and
                volume[i-1] > volume[i-2] and wrb[i] == -1):
            result[i] = -1
    return result
