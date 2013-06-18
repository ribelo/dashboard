#-*- coding: utf-8-*-

import numpy as np
from numba.decorators import jit
from numba import double, int64, int8
from app.tool import deepthroat as dt
from .toolbox import *
from app.config import QUANTUM_CONTRACTION, QUANTUM_LOOK_BACK


@jit(int8[:](double[:], double[:], double[:], double[:], int8[:],
             double[:], int64[:], int64[:], int8[:], int8[:]))
def swing_point1(open, high, low, close, dir,
                 body_size, filled_by, bars_broken_by_body,
                 wrb, wrb_hg):
    """Calculate wrb swing point def 1 zone

    Parameters
    ----------
    candle open: int64[:]
    candle high: int64[:]
    candle low: double[:]
    candle close: double[:]
    candle dir: int8[:]
    candle body size: double[:]
    candle filled by candle: int64[:]
    candle bars broken by body: int64[:]
    candle wrb: int8[:]
    candle wrb hg: int8[:]

    Returns
    -------
    int8[:] where
    bear swing point = -1
    no swing point = 0
    bull swing point = 1
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for v1 in range(4, size):
        # Look for V1 WRB HG
        if wrb_hg[v1]:
            continue
        # Look for V2
        for v2 in range(v1 - 4, v1 - QUANTUM_CONTRACTION, -1):  # 4 + 64 = 68
            # Bullish Swing Point
            # V2 must be wrb or wrb hg
            if (dir[v1] == 1 and (wrb[v2] or wrb_hg[v2]) and
                # V1 must produce min 2 consecutive bull candles close above
                volatility_expand_after(v1, open, high, low, close, dir) and
                # Contraction volatility must share min 1 pip with V2
                contraction_share(v1, v2, high, low) and
                # V1 must breakout volatility contraction
                contraction_break(v1, v2, bars_broken_by_body) and
                # Body of V1/V2 must be greater than volatiliti
                # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        # Price action must fill prior Bear WRB HG. Thus, the prior
                # WRB HG must occur before the v2 WRB
                prior_wrb = prior_bear_wrb_hg(v2, dir, wrb_hg)
                if fill_prior_wrb_hg(v1, prior_wrb, filled_by):
                    # Bear V2
                    if dir[v2] == -1:
                        result[v1] = 1
                        break
                    # Bull V2
                    elif dir[v2] == 1:
                        swing_point = v2 if low[v2] < low[v2 - 1] else v2 - 1
                        if is_bull_swing_point(swing_point, prior_wrb, low):
                            result[v1] = 1
                            break
            # Bearish Swing Point
            # V2 must be wrb or wrb hg
            elif (dir[v1] == -1 and (wrb[v2] or wrb_hg[v2]) and
                  # V1 must produce min 2 consecutive bear candles close
                  # belove
                  volatility_expand_after(v1, open, high, low, close, dir) and
                  # Contraction volatility must share min 1 pip with V2
                  contraction_share(v1, v2, high, low) and
                  # V1 must breakout volatility contraction
                  contraction_break(v1, v2, bars_broken_by_body) and
                  # Body of V1/V2 must be greater than volatiliti
                  # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                # Price action must fill prior Bear WRB HG. Thus, the prior
                # WRB HG must occur before the v2 WRB
                prior_wrb = prior_bull_wrb_hg(v2, dir, wrb_hg)
                if fill_prior_wrb_hg(v1, prior_wrb, filled_by):
                    # Bull V2
                    if dir[v2] == 1:
                        result[v1] = -1
                        break
                    # Bear V2
                    elif dir[v2] == -1:
                        swing_point = v2 if high[
                            v2] > high[v2 - 1] else v2 - 1
                        if is_bear_swing_point(swing_point, prior_wrb, high):
                            result[v1] = -1
                            break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:], int8[:],
             double[:], int64[:], int8[:], int8[:]))
def swing_point2(open, high, low, close, dir,
                 body_size, bars_broken_by_body, wrb, wrb_hg):
    """Calculate wrb swing point def 2 zone

    Parameters
    ----------
    candle open: int64[:]
    candle high: int64[:]
    candle low: double[:]
    candle close: double[:]
    candle dir: v[:]
    candle body size: double[:]
    candle filled by candle: int64[:]
    candle bars broken by body: int64[:]
    candle wrb: int8[:]
    candle wrb hg: int8[:]

    Returns
    -------
    int8[:]
    bear swing point = -1
    no swing point = 0
    bull swing point = 1
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for v1 in range(4, size):
        # Look for V1 WRB HG
        if not wrb_hg[v1]:
            continue
        # Look for V2
        for v2 in range(v1 - 4, v1 - QUANTUM_CONTRACTION, -1):  # 4 + 64 = 68
            # Bullish Swing Point
            if (dir[v1] == 1 and
                # V2 must be wrb or wrb hg and v2 must be bear
                (wrb[v2] == -1 or wrb_hg[v2] == -1) and
                # V1 must produce strong volatiliti expand
                volatility_strong_expand_after(v1, close, dir) and
                # Contraction volatility must share min 1 pip with V2
                contraction_share(v1, v2, high, low) and
                # V1 must breakout volatility contraction
                contraction_break(v1, v2, bars_broken_by_body) and
                # Body of V1/V2 must be greater than volatiliti
                # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = 1
                break
            # Bearish Swing Point
            elif (dir[v1] == -1 and
                  # V2 must be wrb or wrb hg and v2 must be bear
                  (wrb[v2] == 1 or wrb_hg[v2] == 1) and
                  # V1 must produce strong volatiliti expand
                  volatility_strong_expand_after(v1, close, dir) and
                  # Contraction volatility must share min 1 pip with V2
                  contraction_share(v1, v2, high, low) and
                  # V1 must breakout volatility contraction
                  contraction_break(v1, v2, bars_broken_by_body) and
                  # Body of V1/V2 must be greater than volatiliti
                  # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = -1
                break
    return result


@jit(int8[:](double[:], double[:], double[:], int8[:], double[:],
             int8[:], int64[:], int8[:]))
def strong_continuation1(open, high, low, dir, body_size, reaction_break,
                         bars_broken_by_body, wrb_hg):
    """Calculate wrb strong continuation def 1 zone

    Parameters
    ----------
    candle open: int64[:]
    candle high: int64[:]
    candle low: double[:]
    candle dir: int64[:]
    candle body size: double[:]
    candle reaction_break: int8[:]
    candle bars broken by body: int64[:]
    candle wrb hg: int64[:]

    Returns
    -------
    int64[:] where
    strong continuation = 1
    no strong continuation = 0
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for v1 in range(4, size):
        # Look for V1 WRB HG
        if not wrb_hg[v1]:
            continue
        # Bullish Swing Point
        # Look for V2
        for v2 in range(v1 - 4, v1 - QUANTUM_CONTRACTION, -1):  # 4 + 64 = 68
            # V2 wrb hg and must be bull
            if (dir[v1] == 1 and wrb_hg[v2] == 1 and
                # Contraction volatility must share min 1 pip with V2
                contraction_share(v1, v2, high, low) and
                # V1 must breakout volatility contraction
                contraction_break(v1, v2, bars_broken_by_body) and
                # Body of V1/V2 must be greater than volatiliti
                # contraction
                contraction_body_size_break(v1, v2, body_size) and
                # V1 or V2 must be bull reaction break
                    (reaction_break[v1] or reaction_break[v2])):
                result[v1] = 1
                break
            # Bearish Swing Point
            # V2 wrb hg and must be bear
            elif (dir[v1] == -1 and wrb_hg[v2] == -1 and
                  # Contraction volatility must share min 1 pip with V2
                  contraction_share(v1, v2, high, low) and
                  # V1 must breakout volatility contraction
                  contraction_break(v1, v2, bars_broken_by_body) and
                  # Body of V1/V2 must be greater than volatiliti
                  # contraction
                  contraction_body_size_break(v1, v2, body_size) and
                  # V1 or V2 must be bull reaction break
                    (reaction_break[v1] or reaction_break[v2])):
                result[v1] = -1
                break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:], int8[:], double[:],
             int64[:], int8[:]))
def strong_continuation2(open, high, low, close, dir, body_size,
                         bars_broken_by_body, wrb_hg):
    """Calculate wrb strong continuation def 2 zone

    Parameters
    ----------
    candle open: int64[:]
    candle high: int64[:]
    candle low: double[:]
    candle dir: int64[:]
    candle body size: double[:]
    candle bars broken by body: int64[:]
    candle wrb hg: int64[:]

    Returns
    -------
    int64[:] where
    strong continuation = 1
    no strong continuation = 0
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for v1 in range(4, size):
        # Look for V1 WRB HG
        if not wrb_hg[v1]:
            continue
        # Bullish Swing Point
        # Look for V2
        for v2 in range(v1 - 4, v1 - QUANTUM_CONTRACTION, -1):  # 4 + 64 = 68
            # V2 wrb hg and must be bull
            if (dir[v1] == 1 and wrb_hg[v2] == 1 and
                # Must be volatiliti expand after v1
                volatility_week_expand_after(v1, close, dir) and
                # Must be volatiliti expand before v2
                volatility_week_expand_before(v2, close, dir) and
                # Volatiliti contraction cant retrace 3 interval befor v2
                not contraction_retrace(v1, v2, 3, high, low, dir) and
                # Contraction volatility must share min 1 pip with V2
                contraction_share(v1, v2, high, low) and
                # V1 must breakout volatility contraction
                contraction_break(v1, v2, bars_broken_by_body) and
                # Body of V1/V2 must be greater than volatiliti
                # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = 1
                break
            # Bearish Swing Point
            # V2 wrb hg and must be bear
            elif (dir[v1] == -1 and wrb_hg[v2] == -1 and
                  # Must be volatiliti expand after v1
                  volatility_week_expand_after(v1, close, dir) and
                  # Must be volatiliti expand before v2
                  volatility_week_expand_before(v2, close, dir) and
                  # Volatiliti contraction cant retrace 3 interval befor v2
                  not contraction_retrace(v1, v2, 3, high, low, dir) and
                  # Contraction volatility must share min 1 pip with V2
                  contraction_share(v1, v2, high, low) and
                  # V1 must breakout volatility contraction
                  contraction_break(v1, v2, bars_broken_by_body) and
                  # Body of V1/V2 must be greater than volatiliti
                  # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = -1
                break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:], int8[:], double[:],
             double[:], int64[:], int8[:]))
def strong_continuation3(open, high, low, close, dir, body_size,
                         body_mid_point, bars_broken_by_body, wrb_hg):
    """Calculate wrb strong continuation def 3 zone

    Parameters
    ----------
    candle open: int64[:]
    candle high: int64[:]
    candle low: double[:]
    candle dir: int64[:]
    candle body size: double[:]
    candle bars broken by body: int64[:]
    candle wrb hg: int64[:]

    Returns
    -------
    int64[:] where
    strong continuation = 1
    no strong continuation = 0
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for v1 in range(4, size):
        # Look for V1 WRB HG
        if not wrb_hg[v1]:
            continue
        # Bullish Swing Point
        # Look for V2
        for v2 in range(v1 - 4, v1 - QUANTUM_CONTRACTION, -1):  # 4 + 64 = 68
            # V2 wrb hg and must be bull
            if (dir[v1] == 1 and wrb_hg[v2] == 1 and
                # v2 must have the bodies of the prior contracting volatility
                # < body mid-point of v2 or v1 must have the bodies of the prior
                # contracting volatility < body mid-point of v1
                (body_mid_point[v2] > dt.nanmax(close[v2 - 1:v2 - 4]) or
                 body_mid_point[v1] > dt.nanmin(close[v2 + 1:v1])) and
                # Contraction volatility must share min 1 pip with V2
                contraction_share(v1, v2, high, low) and
                # V1 must breakout volatility contraction
                contraction_break(v1, v2, bars_broken_by_body) and
                # Body of V1/V2 must be greater than volatiliti
                # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = 1
                break
            # Bearish Swing Point
            # V2 wrb hg and must be bear
            elif (dir[v1] == -1 and wrb_hg[v2] == -1 and
                  # v2 must have the bodies of the prior contracting volatility
                  # body mid-point of v2 or v1 must have the bodies of the
                  # prior contracting volatility < body mid-point of v1
                  (body_mid_point[v2] < dt.nanmin(close[v2 - 1:v2 - 4]) or
                   body_mid_point[v1] < dt.nanmin(close[v2 + 1:v1])) and
                  # Contraction volatility must share min 1 pip with V2
                  contraction_share(v1, v2, high, low) and
                  # V1 must breakout volatility contraction
                  contraction_break(v1, v2, bars_broken_by_body) and
                  # Body of V1/V2 must be greater than volatiliti
                  # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = -1
                break
    return result


@jit(int8[:](double[:], double[:], double[:], double[:], int8[:], double[:],
             double[:], int64[:], int8[:]))
def strong_continuation4(open, high, low, close, dir, body_size,
                         body_mid_point, bars_broken_by_body, wrb_hg):
    """Calculate wrb strong continuation def 3 zone

    Parameters
    ----------
    candle open: int64[:]
    candle high: int64[:]
    candle low: double[:]
    candle dir: int64[:]
    candle body size: double[:]
    candle bars broken by body: int64[:]
    candle wrb hg: int64[:]

    Returns
    -------
    int64[:] where
    strong continuation = 1
    no strong continuation = 0
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int8)

    for v1 in range(4, size):
        # Look for V1 WRB HG
        if not wrb_hg[v1]:
            continue
        # Bullish Swing Point
        # Look for V2
        for v2 in range(v1 - 4, v1 - QUANTUM_CONTRACTION, -1):  # 4 + 64 = 68
            # V2 wrb hg and must be bull
            if (dir[v1] == 1 and wrb_hg[v2] == 1 and
                # V1 body > V2 body and close V1 > close V2
                body_size[v1] > body_size[v2] and close[v1] > close[2] and
                body_mid_point[v2] > dt.nanmin(close[v2 + 1:v1]) and
                # Contraction volatility must share min 1 pip with V2
                contraction_share(v1, v2, high, low) and
                # V1 must breakout volatility contraction
                contraction_break(v1, v2, bars_broken_by_body) and
                # Body of V1/V2 must be greater than volatiliti
                # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = 1
                break
            # Bearish Swing Point
            # V2 wrb hg and must be bear
            elif (dir[v1] == -1 and wrb_hg[v2] == -1 and
                  # V1 body > V2 body and close V1 > close V2
                  body_size[v1] > body_size[v2] and close[v1] > close[2] and
                  body_mid_point[v2] < dt.nanmin(close[v2 + 1:v1]) and
                  # Contraction volatility must share min 1 pip with V2
                  contraction_share(v1, v2, high, low) and
                  # V1 must breakout volatility contraction
                  contraction_break(v1, v2, bars_broken_by_body) and
                  # Body of V1/V2 must be greater than volatiliti
                  # contraction
                    contraction_body_size_break(v1, v2, body_size)):
                result[v1] = -1
                break
    return result


@jit(int64[:](double[:], double[:], double[:], double[:], int64[:], int64[:]))
def inside_zone(open, high, low, close, filled_by, zones):
    """Look for canldes inside wrb zone

    Parameters
    ----------
    candle high: double[:]
    candle low: double[:]
    candle filled by candle: int64[:]
    candle zones: int8[:]

    Returns
    -------
    int64[:]
    nr of candle zone
    """

    size = open.shape[0]
    result = np.zeros(size, dtype=np.int64)

    for i in range(size):
        for j in range(1, min(QUANTUM_LOOK_BACK, i - QUANTUM_LOOK_BACK)):
            if (zones[i-j] > 0 and ((high[i] > open[i-j] and high[i] < close[i-j])
                or (low[i] > open[i-j] and low[i] < close[i-j])) and
                    filled_by[i - j] > i):
                        result[i] = i - j
                        break
            elif (zones[i-j] < 0 and ((high[i] > close[i-j] and high[i] < open[i-j])
                  or (low[i] > close[i-j] and low[i] < open[i-j])) and
                    filled_by[i - j] > i):
                        result[i] = i - j
                        break
    return result
