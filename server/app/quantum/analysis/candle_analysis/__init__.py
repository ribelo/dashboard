#-*- coding: utf-8-*-
import bottleneck as bn
from . import base


def calculate(df, vol_avg=True, dir=True, body_size=True,
              body_size_break=True, body_mid_point=True, bar_size=True,
              bar_size_break=True, bars_broken_by_body=True,
              bar_mid_point=True, shadow_upper=True, shadow_lower=True,
              filled_by=True, broken_by=True, *args, **kwds):

    assert 'open' in df, 'DataFrame must have open column'
    assert 'high' in df, 'DataFrame must have high column'
    assert 'low' in df, 'DataFrame must have low column'
    assert 'close' in df, 'DataFrame must have close column'

    if vol_avg:
        df['volume_average'] = bn.move_mean(df['volume'], 14)
    if dir:
        df['dir'] = base.dir(df['open'], df['close'])
    if body_size:
        df['body_size'] = base.body_size(df['open'], df['close'])
    if body_size_break:
        assert 'body_size' in df, 'DataFrame must have body_size column'
        df['body_size_break'] = base.body_size_break(df['body_size'])
    if body_mid_point:
        df['body_mid_point'] = base.body_mid_point(df['open'], df['close'])
    if bar_size:
        df['bar_size'] = base.bar_size(df['high'], df['low'])
    if bar_size_break:
        assert 'bar_size' in df, 'DataFrame must have bar_size column'
        df['bar_size_break'] = base.bar_size_break(df['bar_size'])
    if bars_broken_by_body:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['bars_broken_by_body'] = base.bars_broken_by_body(
            df['high'], df['low'], df['close'], df['dir'])
    if bar_mid_point:
        df['bar_mid_point'] = base.bar_mid_point(df['high'], df['low'])
    if filled_by:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['filled_by'] = base.filled_by(df['open'], df['high'],
                                           df['low'], df['dir'])
    if broken_by:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['broken_by'] = base.broken_by(df['high'], df['low'],
                                           df['close'], df['dir'])