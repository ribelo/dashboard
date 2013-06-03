from numba import double, int64, int8, bool_
from numba.decorators import jit
import tool.deepthroat as dt


@jit(bool_(int64, int64, double[:], double[:]), nopython=True)
def contraction_share(v1, v2, high, low):
    """Calculate does v2 shares min 1 pip with volatility contraction

    Parameters
    ----------
    candle v1: int
    candle v2: int
    candle high: double[:]
    candle low: double[:]

    Returns
    -------
    True if share False if doesn't
    """
    for i in range(v1, v2, -1):
        if high[v2] < low[i] and low[v2] > high[i]:
            return False
    else:
        return True


@jit(int64(int64, int64[:], int8[:]), nopython=True)
def prior_bull_wrb(start, dir, wrb):
    for i in range(start - 1, 0, -1):
        if wrb[i] == 1 and dir[i] == 1:
            return i
    return 0


@jit(int64(int64, int64[:], int8[:]), nopython=True)
def prior_bear_wrb(start, dir, wrb):
    for i in range(start - 1, 0, -1):
        if wrb[i] == 1 and dir[i] == -1:
            return i
    return 0


@jit(int64(int64, int8[:], int8[:]), nopython=True)
def prior_bull_wrb_hg(start, dir, wrb_hg):
    for i in range(start - 1, 0, -1):
        if wrb_hg[i] == 1 and dir[i] == 1:
            return i
    return 0


@jit(int64(int64, int8[:], int8[:]), nopython=True)
def prior_bear_wrb_hg(start, dir, wrb_hg):
    for i in range(start - 1, 0, -1):
        if wrb_hg[i] == 1 and dir[i] == -1:
            return i
    return 0


@jit(bool_(int64, int64, int64[:]), nopython=True)
def fill_prior_wrb_hg(v1, prior_wrb, filled_by):
    """Calculate does v1 fill prior wrb hg

    Parameters
    ----------
    candle v1: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]
    candle v1_dir: int64

    Returns
    -------
    True if fill False if doesn't
    """
    if (filled_by[prior_wrb] >= v1 or
            filled_by[prior_wrb] <= filled_by[v1]):
        return True
    else:
        return False


@jit(int64(int64, int64, int64[:]), nopython=True)
def contraction_break(v1, v2, bars_broken_by_body):
    return bars_broken_by_body[v1] > v1 - v2 - 1


@jit(bool_(int64, int64, double[:]), nopython=True)
def contraction_body_size_break(v1, v2, body_size):
    max_val = body_size[v1] if body_size[v1] > body_size[v2] else body_size[v2]
    max_arr = 0
    for i in range(v2, v1):
        max_arr = body_size[i] if body_size[i] > max_arr else max_arr
    return True if max_val > max_arr else False


@jit(bool_(int64, int64, double[:]), nopython=True)
def is_bull_swing_point(i, end, low):
    for j in range(i, end, -1):
        if low[j] < low[i]:
            return False
    else:
        return True


@jit(bool_(int64, int64, double[:]), nopython=True)
def is_bear_swing_point(i, end, high):
    for j in range(i, end, -1):
        if high[j] > high[i]:
            return False
    else:
        return True


@jit(bool_(int64, double[:], int8[:]), nopython=True)
def volatility_week_expand_after(candle, close, dir):
    """Look for volatility expand on right side of candle

    Parameters
    ----------
    candle candle: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]

    Returns
    -------
    True if produce False if doesn't
    """
    cc = 0
    if dir[candle] == 1:
        for i in range(candle + 1, candle + 33):  # 1 + 32 = 33
            # Candle must be bull and close above candle
            if dir[i] == 1 and close[i] > close[candle]:
                cc += 1
            if cc >= 2:
                return True
    elif dir[candle] == -1:
        for i in range(candle + 1, candle + 33):  # 1 + 32 = 33
            # Candle must be bull and close above candle
            if dir[i] == -1 and close[i] < close[candle]:
                cc += 1
            if cc >= 2:
                return True
    return False


@jit(bool_(int64, double[:], int8[:]), nopython=True)
def volatility_week_expand_before(candle, close, dir):
    """Look for volatility expand on left side of candle

    Parameters
    ----------
    candle candle: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]

    Returns
    -------
    True if produce False if doesn't
    """
    cc = 0
    if dir[candle] == 1:
        for i in range(candle - 1, candle - 33, -1):  # 1 + 32 = 33
                # Candle must be bull and close above candle
                if dir[i] == 1 and close[i] < close[candle]:
                    cc += 1
                if cc >= 2:
                    return True
    elif dir[candle] == -1:
        for i in range(candle - 1, candle - 33, -1):  # 1 + 32 = 33
                # Candle must be bull and close belove candle
                if dir[i] == -1 and close[i] > close[candle]:
                    cc += 1
                if cc >= 2:
                    return True
    return False


@jit(bool_(int64, double[:], double[:], double[:], double[:], int8[:]), nopython=True)
def volatility_expand_after(candle, open, high, low, close, dir):
    """Look for volatility expand on right side of candle

    Parameters
    ----------
    candle candle: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]

    Returns
    -------
    True if produce False if doesn't
    """
    if dir[candle] == 1:
        for i in range(candle + 1, candle + 33):  # 1 + 32 = 33
                # Candle must by unfiled
                if low[i] <= open[candle]:
                    return False
                # Candle must be bull and close above candle
                if (dir[i] == 1 and dir[i + 1] == 1 and
                        close[i] > close[candle] and close[i + 1] > close[candle]):
                    return True
    elif dir[candle] == -1:
        for i in range(candle + 1, candle + 33):  # 1 + 32 = 33
                # candle must by unfiled
                if high[i] >= open[candle]:
                    return False
                # Candle must be bull and close belove candle
                if (dir[i] == -1 and dir[i + 1] == -1 and
                        close[i] < close[candle] and close[i + 1] < close[candle]):
                    return True
    return False


@jit(bool_(int64, double[:], double[:], double[:], double[:], int8[:]), nopython=True)
def volatility_expand_before(candle, open, high, low, close, dir):
    """Look for volatility expand on left side of candle

    Parameters
    ----------
    candle candle: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]

    Returns
    -------
    True if produce False if doesn't
    """
    if dir[candle] == 1:
        for i in range(candle - 1, candle - 33, -1):  # 1 + 32 = 33
                # candle must by unfiled
                if high[i] >= close[candle]:
                    return False
                # Candle must be bull and close above candle
                if (dir[i] == 1 and dir[i + 1] == 1 and
                        close[i] > close[candle] and close[i + 1] > close[candle]):
                    return True
    elif dir[candle] == -1:
        for i in range(candle - 1, candle - 33, -1):  # 1 + 32 = 33
                # candle must by unfiled
                if low[i] <= open[candle]:
                    return False
                # Candle must be bull and close belove candle
                if (dir[i] == -1 and dir[i + 1] == -1 and
                        close[i] < close[candle] and close[i + 1] < close[candle]):
                    return True
    return False


@jit(bool_(int64, double[:], int8[:]), nopython=True)
def volatility_strong_expand_after(candle, close, dir):
    """Look for volatility expand on right side of candle:

    Parameters
    ----------
    candle candle: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]

    Returns
    -------
    True if produce False if doesn't
    """
    if dir[candle] == 1:
        if close[candle + 2] > close[candle + 1] > close[candle]:
            return True
    elif dir[candle] == -1:
        if close[candle + 2] < close[candle + 1] < close[candle]:
            return True
    return False


@jit(bool_(int64, double[:], int8[:]), nopython=True)
def volatility_strong_expand_before(candle, close, dir):
    """Look for volatility expand on left side of candle:

    Parameters
    ----------
    candle candle: int
    candle v2: int
    candle wrb_hg: int64[:]
    candle filled_by: int64[:]
    candle dir: int64[:]

    Returns
    -------
    True if produce False if doesn't
    """
    if dir[candle] == 1:
        if close[candle - 2] < close[candle - 1] < close[candle]:
            return True
    elif dir[candle] == -1:
        if close[candle - 2] > close[candle + 1] > close[candle]:
            return True
    return False


@jit(int64(int64, int64, int64, double[:], double[:], int8[:]), nopython=True)
def contraction_retrace(v1, v2, count, high, low, dir):
    if dir[v2] == 1:
        return dt.nanmin(low[v2 - 1 - count:v2 - 1]) <= dt.nanmin(low[v2 + 1:v1])
    elif dir[v2] == -1:
        return dt.nanmax(high[v2 - 1 - count:v2 - 1]) >= dt.nanmax(high[v2 + 1:v1])


@jit(bool_(int64, int64, double[:], double[:], int8[:]))
def contraction_fill(v1, v2, high, low, dir):
    if dir[v2] == 1:
        if dt.nanmin(low[v2+1:v1]) <= open[v2]:
            return True
    elif dir[v2] == -1:
        if dt.nanmax(high[v2+1:v1]) >= open[v2]:
            return True
    return False
