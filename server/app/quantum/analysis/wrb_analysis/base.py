#-*- coding: utf-8-*-
import numpy as np
from numba.decorators import jit
from numba import double, int64, int8, bool_


@jit(double[:](double[:], double[:], double[:], double[:]))
def gap(open, high, low, close):
    """Calculate hiden gap betwen candles

    Parameters
    ----------
    candle open: double[:]
    candle high: double[:]
    candle low: double[:]
    candle close: double[:]

    Returns
    -------
    double[:]

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(1, size - 1):
        if open[i + 1] > open[i - 1] and close[i + 1] > close[i - 1]:
            r = low[i + 1] - high[i - 1]
            if r > 0:
                result[i] = r
        elif open[i + 1] < open[i - 1] and close[i + 1]:
            r = low[i - 1] - high[i + 1]
            if r > 0:
                result[i] = r

    return result


@jit(bool_[:](double[:], int8[:]))
def reaction_high(high, dir):
    """Calculate candle reaction high

    Parameters
    ----------
    candle high: double[:]
    candle dir: int8[:]

    Returns
    -------
    int8[:] where
    bull reaction = 1
    no reaction = 0
    """

    size = high.shape[0]
    result = np.zeros(size, dtype=np.bool_)

    for i in range(3, size - 3):
        reaction = high[i]
        cr = 0  # candle rising
        cf = 0  # candle falling
        for j in range(1, max(65, i)):
            if i - j < 0 or i + j >= size:
                break
            if (high[i-j] > reaction
                    or high[i+j] > reaction
                    or i + j > size
                    or i - j < 0):
                break
            if cr < 2:
                if dir[i-j] == 1:
                    cr += 1
                else:
                    cr = 0
            if cf < 2:
                if dir[i+j] == -1:
                    cf += 1
                else:
                    cf = 0
            if cf >= 2 and cr >= 2:
                result[i] = True
                break

    return result


@jit(bool_[:](double[:], int64[:]))
def reaction_low(low, dir):
    """Calculate candle reaction low

    Parameters
    ----------
    candle low: double[:]
    candle dir: int64[:]

    Returns
    -------
    int64[:] where
    no reaction = 0
    bear reaction = -1
    """

    size = low.shape[0]
    result = np.zeros(size, dtype=np.bool_)

    for i in range(3, size - 3):
        reaction = low[i]
        cr = 0  # candle rising
        cf = 0  # candle falling
        for j in range(1, max(65, i)):
            if i - j < 0 or i + j >= size:
                break
            if (low[i-j] < reaction
                    or low[i+j] < reaction
                    or i + j > size
                    or i - j < 0):
                break
            if cr < 2:
                if dir[i+j] == 1:
                    cr += 1
                else:
                    cr = 0
            if cf < 2:
                if dir[i-j] == -1:
                    cf += 1
                else:
                    cf = 0
            if cf >= 2 and cr >= 2:
                result[i] = True
                break

    return result


@jit(int8[:](double[:], double[:], double[:], int8[:], int64[:],
              bool_[:], bool_[:]))
def reaction_break(high, low, close, dir, broken_by,
                   reaction_high, reaction_low):
    size = low.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        if dir[i] == 1:
            for j in range(1, max(65, i)):  # 65-1=64
                if close[i] <= high[i-j]:
                    break
                if (reaction_high[i-j] == -1 and
                        broken_by[i-j] == i):
                    result[i] = 1
                    break
        elif dir[i] == -1:
            for j in range(1, max(65, i)):  # 65-1=64
                if close[i] >= low[i-j]:
                    break
                if (reaction_low[i-j] == 1 and
                        broken_by[i-j] == i):
                    result[i] = -1
                    break
    return result


@jit(int8[:](int8[:], int64[:], int64[:]))
def wrb(dir, body_size_break, bars_broken_by_body):
    """Calculate wrb candles

    Parameters
    ----------
    candle dir: int8[:]
    candle body size break: int64[:]
    candle bars broken by body: int64[:]

    Returns
    -------
    int64[:] where
    wrb = 1
    no wrb = 0
    """

    size = body_size_break.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        if body_size_break[i] >= 3 and bars_broken_by_body[i] >= 3:
            if dir[i] == 1:
                result[i] = 1
            elif dir[i] == -1:
                result[i] = -1

    return result


@jit(int8[:](int8[:], int8[:], double[:]))
def wrb_hg(dir, wrb, gap):
    """Calculate wrb hidden gap candles

    Parameters
    ----------
    candle dir: int8[:]
    candle wrb: int8[:]
    candle gap: double[:]

    Returns
    -------
    int8[:]
    wrb_hg bull = 1
    no wrb_hg = 0
    wrb_hg bear = -1
    """

    size = wrb.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        if wrb[i] and gap[i]:
            if dir[i] == 1:
                result[i] = 1
            elif dir[i] == -1:
                result[i] = -1

    return result
