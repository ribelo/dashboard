#-*- coding: utf-8-*-
from .analysis import candle_analysis as candle
from .analysis import wrb_analysis as wrba
from .analysis.wrb_analysis import zone


def candle_analysis(df, dir=True, body_size=True, body_size_break=True,
                    body_mid_point=True, bar_size=False, bar_size_break=False,
                    bars_broken_by_body=True, bar_mid_point=False,
                    shadow_upper=True, shadow_lower=True, filled_by=True,
                    broken_by=True, *args, **kwds):

    assert 'open' in df, 'DataFrame must have open column'
    assert 'high' in df, 'DataFrame must have high column'
    assert 'low' in df, 'DataFrame must have low column'
    assert 'close' in df, 'DataFrame must have close column'

    if dir:
        df['dir'] = candle.dir(df['open'], df['close'])
    if body_size:
        df['body_size'] = candle.body_size(df['open'], df['close'])
    if body_size_break:
        assert 'body_size' in df, 'DataFrame must have body_size column'
        df['body_size_break'] = candle.body_size_break(df['body_size'])
    if body_mid_point:
        df['body_mid_point'] = candle.body_mid_point(df['open'], df['close'])
    if bar_size:
        df['bar_size'] = candle.bar_size(df['high'], df['low'])
    if bar_size_break:
        assert 'bar_size' in df, 'DataFrame must have bar_size column'
        df['bar_size_break'] = candle.bar_size_break(df['bar_size'])
    if bars_broken_by_body:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['bars_broken_by_body'] = candle.bars_broken_by_body(
            df['high'], df['low'], df['close'], df['dir'])
    if bar_mid_point:
        df['bar_mid_point'] = candle.bar_mid_point(df['high'], df['low'])
    if filled_by:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['filled_by'] = candle.filled_by(df['open'], df['high'],
                                           df['low'], df['dir'])
    if broken_by:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['broken_by'] = candle.broken_by(df['high'], df['low'],
                                           df['close'], df['dir'])


def wrb_analysis(df, gap=True, reaction=True, reaction_break=True,
                 wrb=True, wrb_hg=True, *args, **kwds):

    assert 'open' in df, 'DataFrame must have open column'
    assert 'high' in df, 'DataFrame must have high column'
    assert 'low' in df, 'DataFrame must have low column'
    assert 'close' in df, 'DataFrame must have close column'

    if gap:
        df['gap'] = wrba.gap(df['open'], df['high'], df['low'], df['close'])
    if reaction:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['reaction'] = wrba.reaction(df['high'], df['low'], df['dir'])
    if reaction_break:
        assert 'dir' in df, 'DataFrame must have dir column'
        assert 'broken_by' in df, 'DataFrame must have broken_by column'
        assert 'reaction' in df, 'DataFrame must have reaction column'
        df['reaction_break'] = wrba.reaction_break(df['high'], df['low'],
                                                  df['close'], df['dir'],
                                                  df['broken_by'],
                                                  df['reaction'])
    if wrb:
        assert 'body_size_break' in df, 'DataFrame must have body_size_break \
                                         column'
        assert 'bars_broken_by_body' in df, 'DataFrame must have \
                                             bars_broken_by_body column'
        df['wrb'] = wrba.wrb(df['body_size_break'], df['bars_broken_by_body'])
    if wrb_hg:
        assert 'wrb' in df, 'DataFrame must have wrb column'
        assert 'gap' in df, 'DataFrame must have gap column'
        df['wrb_hg'] = wrba.wrb_hg(df['wrb'], df['gap'])
