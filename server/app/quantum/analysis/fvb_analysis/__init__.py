from . import fvb


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
