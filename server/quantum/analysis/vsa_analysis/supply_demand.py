#-*- coding: utf-8-*-
import numpy as np
from numba.decorators import jit
from numba import double, int64, int8
from server.config import QUANTUM_LOOK_BACK


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd1(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and volume[i] < volume[i-1] and
            volume[i] < volume[i-2] and close[i] < close[i+1] and
                low[i] <= low[i+1]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and volume[i] < volume[i-1] and
              volume[i] < volume[i-2] and close[i] > close[i+1] and
                high[i] >= high[i+1]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd2(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] > bar_size[i-1] and close[i] == open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] > bar_size[i-1] and close[i] == open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd3(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] > bar_size[i-1] and close[i] == high[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] > bar_size[i-1] and close[i] == high[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd4(open, high, low, close, volume, bar_size,
          bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] > bar_size[i-1] and
            close[i] == bar_mid_point[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] > bar_size[i-1] and
              close[i] == bar_mid_point[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd5(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] > bar_size[i-1] and close[i] == high[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] > bar_size[i-1] and close[i] == low[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd6(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] < close[i-1] and bar_size[i] < bar_size[i-1] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] > close[i-1] and bar_size[i] < bar_size[i-1] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd7(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] < close[i-1] and bar_size[i] == bar_size[i-1] and
            close[i] == open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] < volume[i-1] and
                volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] > close[i-1] and bar_size[i] == bar_size[i-1] and
              close[i] == open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] < volume[i-1] and
                volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd8(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] < close[i-1] and bar_size[i] == bar_size[i-1] and
            close[i] == low[i] and close[i] != open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] > close[i-1] and bar_size[i] == bar_size[i-1] and
              close[i] == high[i] and close[i] != open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd9(open, high, low, close, volume, bar_size,
          bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] < close[i-1] and bar_size[i] == bar_size[i-1] and
            close[i] == bar_mid_point[i] and close[i] != open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] > close[i-1] and bar_size[i] == bar_size[i-1] and
              close[i] == bar_mid_point[i] and close[i] != open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd10(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] < close[i-1] and bar_size[i] == bar_size[i-1] and
            close[i] == high[i] and close[i] != open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] > close[i-1] and bar_size[i] == bar_size[i-1] and
              close[i] == low[i] and close[i] != open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd11(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
            close[i] == open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] < volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
              close[i] == open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] < volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd12(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
            close[i] == low[i] and close[i] != open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
              close[i] == high[i] and close[i] != open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd13(open, high, low, close, volume, bar_size,
           bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
            close[i] == bar_mid_point[i] and close[i] != open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
              close[i] == bar_mid_point[i] and close[i] != open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd14(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
            close[i] == low[i] and close[i] != open[i] and
            close[i] < close[i+1] and low[i] <= low[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (close[i] == close[i-1] and bar_size[i] < bar_size[i-1] and
              close[i] == low[i] and close[i] != open[i] and
              close[i] > close[i+1] and high[i] >= high[i+1] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd15(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
           bar_size[i] <= bar_size[i-1] and close[i] <= close[i-1] and
           close[i] == open[i] and close[i] == close[i+1] and
           close[i] < close[i+2] and low[i] <= low[i+1] and
           low[i] <= low[i+2] and volume[i] < volume[i-1] and
           volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] >= close[i-1] and
              close[i] == open[i] and close[i] == close[i+1] and
              close[i] > close[i+2] and high[i] >= high[i+1] and
              high[i] >= high[i+2] and volume[i] < volume[i-1] and
                volume[i] < volume[i-2]):
                # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd16(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] <= close[i-1] and
            close[i] == low[i] and close[i] != open[i] and
            close[i] == close[i+1] and close[i] < close[i+2] and
            low[i] <= low[i+1] and low[i] <= low[i+2] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] >= close[i-1] and
              close[i] == high[i] and close[i] != open[i] and
              close[i] == close[i+1] and close[i] > close[i+2] and
              high[i] >= high[i+1] and high[i] >= high[i+2] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd17(open, high, low, close, volume, bar_size, bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] <= close[i-1] and
            close[i] == bar_mid_point[i] and close[i] != open[i] and
            close[i] == close[i+1] and close[i] < close[i+2] and
            low[i] <= low[i+1] and low[i] <= low[i+2] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] >= close[i-1] and
              close[i] == bar_mid_point[i] and close[i] != open[i] and
              close[i] == close[i+1] and close[i] > close[i+2] and
              high[i] >= high[i+1] and high[i] >= high[i+2] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd18(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] <= close[i-1] and
            close[i] == high[i] and close[i] != open[i] and
            close[i] == close[i+1] and close[i] < close[i+2] and
            low[i] <= low[i+1] and low[i] <= low[i+2] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] >= close[i-1] and
              close[i] == low[i] and close[i] != open[i] and
              close[i] == close[i+1] and close[i] > close[i+2] and
              high[i] >= high[i+1] and high[i] >= high[i+2] and
                volume[i] < volume[i-1] and volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd19(open, high, low, close, volume, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            close[i] == open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              close[i] == open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd20(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == low[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == high[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd21(open, high, low, close, volume, bar_size,
           bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == bar_mid_point[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == bar_mid_point[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd22(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == high[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == low[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] < volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd23(open, high, low, close, volume, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            close[i] == open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              close[i] == open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd24(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == low[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == high[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd25(open, high, low, close, volume, bar_size,
           bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == bar_mid_point[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == bar_mid_point[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd26(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == high[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == low[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] < volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd27(open, high, low, close, volume, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            close[i] == open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              close[i] == open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd28(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == low[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == high[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], double[:], int64[:], int8[:]))
def _nsd29(open, high, low, close, volume, bar_size,
           bar_mid_point, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == bar_mid_point[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == bar_mid_point[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result


@jit(int8[:](double[:], double[:], double[:], double[:],
             double[:], double[:], int64[:], int8[:]))
def _nsd30(open, high, low, close, volume, bar_size, filled_by, zones):
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)
    for i in range(1, size - 1):
        # no supply / bull signal
        if (low[i] < low[i-1] and high[i] <= high[i-1] and
            bar_size[i] <= bar_size[i-1] and close[i] == high[i] and
            close[i] != open[i] and close[i] < close[i+1] and
            low[i] <= low[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] > 0 and filled_by[i-j] >= i and
                        (low[i] <= close[i-j])):
                    result[i] = 1
                    break
        # no demand / bear singal
        elif (high[i] > high[i-1] and low[i] >= low[i-1] and
              bar_size[i] <= bar_size[i-1] and close[i] == low[i] and
              close[i] != open[i] and close[i] > close[i+1] and
              high[i] >= high[i+1] and volume[i] == volume[i-1] and
                volume[i] == volume[i-2]):
            # Look for zone
            for j in range(1, min(QUANTUM_LOOK_BACK + 2, i)):  # 64 + 1 = 65
                if (zones[i-j] < 0 and filled_by[i-j] >= i and
                        (high[i] >= close[i-j])):
                    result[i] = -1
                    break

        return result
