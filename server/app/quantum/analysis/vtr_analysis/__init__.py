from . import vtr


def calculate_vtr(df1, df2, invert_sister=False):
    assert 'open' in df1, 'DataFrame must have open column'
    assert 'close' in df1, 'DataFrame must have close column'
    assert 'bar_mid_point' in df1, 'DataFrame must have bar mid point column'
    assert 'filled_by' in df1, 'DataFrame must have filled by column'
    assert 'wrb_hg' in df1, 'DataFrame must have body wrb column'
    assert 'zones' in df1, 'DataFrame must have body zones column'
    assert 'open' in df2, 'DataFrame must have open column'
    assert 'close' in df2, 'DataFrame must have close column'
    assert 'bar_mid_point' in df2, 'DataFrame must have bar mid point column'
    assert 'filled_by' in df2, 'DataFrame must have filled by column'
    assert 'wrb_hg' in df2, 'DataFrame must have body wrb column'
    assert 'zones' in df2, 'DataFrame must have body zones column'
    if not invert_sister:
        temp = vtr.vtr(
            df1['open'], df1['close'], df1['dir'], df1['body_mid_point'],
            df1['filled_by'], df1['wrb_hg'], df1['zones'],
            df2['open'], df2['close'], df2[
                'dir'], df2['body_mid_point'],
            df2['filled_by'], df2['wrb_hg'], df2['zones'])
    else:
        temp = vtr.vtr(
            df1['open'], df1['close'], df1['dir'], df1['body_mid_point'],
            df1['filled_by'], df1['wrb_hg'], df1['zones'],
            pow(df2['open'], -1), pow(df2['close'], -1),
            df2['dir'] * -1, pow(df2['body_mid_point'], -1),
            df2['filled_by'], df2['wrb_hg'] * -1, df2['zones'] * -1)
    df1['vtr'] = temp
    df2['vtr'] = temp
