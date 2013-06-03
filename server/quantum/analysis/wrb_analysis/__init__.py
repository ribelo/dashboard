#-*- coding: utf-8-*-
import pandas as pd
from . import base
from . import zone
from . import fvb


def calculate_base(df, gap=True, reaction=True, reaction_break=True,
                   wrb=True, wrb_hg=True, *args, **kwds):

    assert 'open' in df, 'DataFrame must have open column'
    assert 'high' in df, 'DataFrame must have high column'
    assert 'low' in df, 'DataFrame must have low column'
    assert 'close' in df, 'DataFrame must have close column'

    if gap:
        df['gap'] = base.gap(df['open'], df['high'], df['low'], df['close'])
    if reaction:
        assert 'dir' in df, 'DataFrame must have dir column'
        df['reaction_high'] = base.reaction_high(df['high'], df['dir'])
        df['reaction_low'] = base.reaction_low(df['low'], df['dir'])
    if reaction_break:
        assert 'dir' in df, 'DataFrame must have dir column'
        assert 'broken_by' in df, 'DataFrame must have broken_by column'
        assert 'reaction_high' in df, 'DataFrame must have reaction_high column'
        assert 'reaction_low' in df, 'DataFrame must have reaction_low column'
        df['reaction_break'] = base.reaction_break(df['high'], df['low'],
                                                   df['close'], df['dir'],
                                                   df['broken_by'],
                                                   df['reaction_high'],
                                                   df['reaction_low'])
    if wrb:
        assert 'dir' in df, 'DataFrame must have dir column'
        assert 'body_size_break' in df, 'DataFrame must have body_size_break \
                                         column'
        assert 'bars_broken_by_body' in df, 'DataFrame must have \
                                             bars_broken_by_body column'
        df['wrb'] = base.wrb(df['dir'], df['body_size_break'],
                             df['bars_broken_by_body'])
    if wrb_hg:
        assert 'dir' in df, 'DataFrame must have dir column'
        assert 'wrb' in df, 'DataFrame must have wrb column'
        assert 'gap' in df, 'DataFrame must have gap column'
        df['wrb_hg'] = base.wrb_hg(df['dir'], df['wrb'], df['gap'])


def calculate_zones(df, sp1=True, sp2=True, sc1=True, sc2=True,
                    sc3=True, sc4=True, reaction=True):

    zones = pd.DataFrame(index=df.index)
    if sp1:
        df['swing_point1'] = zone.swing_point1(df['open'], df['high'],
                                               df['low'], df['close'],
                                               df['dir'], df['body_size'],
                                               df['filled_by'],
                                               df['bars_broken_by_body'],
                                               df['wrb'], df['wrb_hg'])
        zones['swing_point1'] = df['swing_point1']
    if sp2:
        df['swing_point2'] = zone.swing_point2(df['open'], df['high'],
                                               df['low'], df['close'],
                                               df['dir'], df['body_size'],
                                               df['bars_broken_by_body'],
                                               df['wrb'], df['wrb_hg'])
        zones['swing_point2'] = df['swing_point2']
    if sc1:
        df['strong_continuation1'] = zone.strong_continuation1(df['open'],
                                                               df['high'],
                                                               df['low'],
                                                               df['dir'],
                                                               df['body_size'],
                                                               df['reaction_break'],
                                                               df['bars_broken_by_body'],
                                                               df['wrb_hg'])
        zones['strong_continuation1'] = df['strong_continuation1']
    if sc2:
        df['strong_continuation2'] = zone.strong_continuation2(df['open'],
                                                               df['high'],
                                                               df['low'],
                                                               df['close'],
                                                               df['dir'],
                                                               df['body_size'],
                                                               df['bars_broken_by_body'],
                                                               df['wrb_hg'])
        zones['strong_continuation2'] = df['strong_continuation2']
    if sc3:
        df['strong_continuation3'] = zone.strong_continuation3(df['open'],
                                                               df['high'],
                                                               df['low'],
                                                               df['close'],
                                                               df['dir'],
                                                               df['body_size'],
                                                               df['body_mid_point'],
                                                               df['bars_broken_by_body'],
                                                               df['wrb_hg'])
        zones['strong_continuation3'] = df['strong_continuation3']
    if sc4:
        df['strong_continuation4'] = zone.strong_continuation4(df['open'],
                                                               df['high'],
                                                               df['low'],
                                                               df['close'],
                                                               df['dir'],
                                                               df['body_size'],
                                                               df['body_mid_point'],
                                                               df['bars_broken_by_body'],
                                                               df['wrb_hg'])
        zones['strong_continuation4'] = df['strong_continuation4']
    df['zones'] = zones.sum(axis=1)


def calculate_fvb(df, basic=True):

    assert 'open' in df, 'DataFrame must have open column'
    assert 'close' in df, 'DataFrame must have close column'
    assert 'dir' in df, 'DataFrame must have dir column'
    assert 'body_size' in df, 'DataFrame must have body size column'
    assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
    assert 'filled_by' in df, 'DataFrame must have filled by column'
    assert 'wrb' in df, 'DataFrame must have body wrb column'
    assert 'zones' in df, 'DataFrame must have body zones column'

    if basic:
        df['fvb'] = fvb.basic(df['open'], df['close'],
                              df['dir'], df['body_size'], df['bar_mid_point'],
                              df['filled_by'], df['wrb'], df['zones'])
