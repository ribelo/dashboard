#-*- coding: utf-8-*-

from numba import double, int64, int8
from numba.decorators import jit
import numpy as np


@jit(int8[:](double[:], double[:]))
def dir(open, close):
    """Calculate candle body size

    Parameters
    ----------
    candle open: double[:]
    candle close: double[:]

    Returns
    -------
    int array where

    bear candle = -1
    flat candle = 0
    bull candle = 1

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for i in range(size):
        if close[i] < open[i]:
            result[i] = -1
        elif close[i] == open[i]:
            result[i] = 0
        elif close[i] > open[i]:
            result[i] = 1

    return result


@jit(double[:](double[:], double[:]))
def body_size(open, close):
    """Calculate candle body size

    Parameters
    ----------
    candle open: double[:]
    candle close: double[:]

    Returns
    -------
    double[:]

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        result[i] = abs(close[i] - open[i])

    return result


@jit(double[:](double[:]))
def body_size_break(body_size):
    """Calculate of how many candles candle has a greater body

    Parameters
    ----------
    candle body size: double[:]

    Returns
    -------
    int64[:]
    """

    size = body_size.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size-1):
        for j in range(1, i):
            if body_size[i] <= body_size[i-j]:
                result[i] = j - 1
                break
        else:
            result[i] = np.PINF

    return result


@jit(double[:](double[:], double[:]))
def body_mid_point(open, close):
    """Calculate candle body mid point

    Parameters
    ----------
    candle open: double[:]
    candle close: double[:]

    Returns
    -------
    double[:]

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        result[i] = (close[i] + open[i]) * .5

    return result


@jit(double[:](double[:], double[:]))
def bar_size(high, low):
    """Calculate candle bar size

    Parameters
    ----------
    candle high: double[:]
    candle low: double[:]

    Returns
    -------
    double[:]

    """
    size = high.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        result[i] = high[i] - low[i]

    return result


@jit(double[:](double[:]))
def bar_size_break(bar_size):
    """Calculate of how many candles candle has a greater bar

    Parameters
    ----------
    candle bar size: double[:]

    Returns
    -------
    int64[:]
    """

    size = bar_size.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(1, size):
        for j in range(1, i):
            if bar_size[i] <= bar_size[i-j]:
                result[i] = j - 1
                break
        else:
            result[i] = np.PINF

    return result


@jit(int64[:](double[:], double[:], double[:], int8[:]))
def bars_broken_by_body(high, low, close, dir):
    """Calculate how many bar extreme were broken by candle close

    Parameters
    ----------
    candle high: double[:]
    candle low: double[:]
    candle close: double[:]
    candle dir: int64[:]

    Returns
    -------
    int64[:]
    """
    size = high.shape[0]
    result = np.zeros(size, dtype=np.int64)

    for i in range(1, size):
        if dir[i] == 1:
            for j in range(i-1, 0, -1):
                if close[i] < high[j]:
                    result[i] = i - j - 1
                    break
            else:
                result[i] = i-1
        elif dir[i] == -1:
            for j in range(i-1, 0, -1):
                if close[i] > low[j]:
                    result[i] = i - j - 1
                    break
            else:
                result[i] = i-1

    return result


@jit(double[:](double[:], double[:]))
def bar_mid_point(high, low):
    """Calculate candle bar mid point

    Parameters
    ----------
    candle high: double[:]
    candle low: double[:]

    Returns
    -------
    double[:]

    """
    size = high.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        result[i] = (high[i] + low[i]) * .5

    return result


@jit(double[:](double[:], double[:], double[:]))
def shadow_upper(open, high, close):
    """Calculate upper shadow size

    Parameters
    ----------
    candle open: double[:]
    candle high: double[:]
    candle close: double[:]

    Returns
    -------
    shadow size: double[:]

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        result[i] = high[i] - max(open[i], close[i])

    return result


@jit(double[:](double[:], double[:], double[:]))
def shadow_lower(open, low, close):
    """Calculate upper shadow size

    Parameters
    ----------
    candle open: double[:]
    candle low: double[:]
    candle close: double[:]

    Returns
    -------
    shadow size: double[:]

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.float64)

    for i in range(size):
        result[i] = max(open[i], close[i]) - low[i]

    return result


@jit(int64[:](double[:], double[:], double[:], int8[:]))
def filled_by(open, high, low, dir):
    """Calculate candle that filled the candle

    Parameters
    ----------
    candle open: double[:]
    candle high: double[:]
    candle low: double[:]
    candle dir: int64[:]

    Returns
    -------
    int64[:]

    """
    size = open.shape[0]
    result = np.zeros(size, dtype=np.int64)

    for i in range(size):
        if dir[i] == 1:
            for j in range(1, size - i):
                if low[i+j] <= open[i]:
                    result[i] = i + j
                    break
            else:
                result[i] = -1
        elif dir[i] == -1:
            for j in range(1, size - i):
                if high[i+j] >= open[i]:
                    result[i] = i + j
                    break
            else:
                result[i] = -1
        elif dir[i] == 0:
            for j in range(1, size - i):
                if low[i+j] <= open[i] or high[i+j] >= open[i]:
                    result[i] = i + j
                    break
            else:
                result[i] = -1
    return result


@jit(int64[:](double[:], double[:], double[:], int8[:]))
def broken_by(high, low, close, dir):
    """Calculate candle that braked the candle

    Parameters
    ----------
    candle high: double[:]
    candle low: double[:]
    candle close: double[:]
    candle dir: int64[:]

    Returns
    -------
    int64[:]

    """
    size = high.shape[0]
    result = np.zeros(size, dtype=np.int64)

    for i in range(size):
        if dir[i] == 1:
            for j in range(1, size - i):
                if close[i+j] >= high[i]:
                    result[i] = i + j
                    break
            else:
                result[i] = -1
        elif dir[i] == -1:
            for j in range(1, size - i):
                if close[i+j] < low[i]:
                    result[i] = i + j
                    break
            else:
                result[i] = -1
        elif dir[i] == 0:
            for j in range(1, size - i):
                if close[i+j] > high[i] or close[i+j] < low[i]:
                    result[i] = i + j
                    break
            else:
                result[i] = -1
    return result
