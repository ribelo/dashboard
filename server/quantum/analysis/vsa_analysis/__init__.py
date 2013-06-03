#-*- coding: utf-8-*-
import pandas as pd
from . import supply_demand
from . import effort


def calculate_supply_demand(
    df, nsd1=True, nsd2=True, nsd3=True, nsd4=True, nsd5=True,
    nsd6=True, nsd7=True, nsd8=True, nsd9=True, nsd10=True,
    nsd11=True, nsd12=True, nsd13=True, nsd14=True, nsd15=True,
    nsd16=True, nsd17=True, nsd18=True, nsd19=True, nsd20=True,
    nsd21=True, nsd22=True, nsd23=True, nsd24=True, nsd25=True,
    nsd26=True, nsd27=True, nsd28=True, nsd29=True, nsd30=True,
        *args, **kwds):

    assert 'open' in df, 'DataFrame must have open column'
    assert 'high' in df, 'DataFrame must have high column'
    assert 'low' in df, 'DataFrame must have low column'
    assert 'close' in df, 'DataFrame must have close column'
    assert 'volume' in df, 'DataFrame must have volumme column'
    assert 'bar_size' in df, 'DataFrame must have bar_size column'
    assert 'filled_by' in df, 'DataFrame must have filled_by column'
    assert 'zones' in df, 'DataFrame must have body zones column'

    temp = pd.DataFrame(index=df.index)
    if nsd1:
        temp['nsd1'] = supply_demand._nsd1(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd2:
        temp['nsd2'] = supply_demand._nsd2(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd3:
        temp['nsd3'] = supply_demand._nsd3(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd4:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd4'] = supply_demand._nsd4(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['bar_mid_point'],
                                           df['filled_by'], df['zones'])
    if nsd5:
        temp['nsd5'] = supply_demand._nsd5(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd6:
        temp['nsd6'] = supply_demand._nsd6(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd7:
        temp['nsd7'] = supply_demand._nsd7(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd8:
        temp['nsd8'] = supply_demand._nsd8(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['filled_by'],
                                           df['zones'])
    if nsd9:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd9'] = supply_demand._nsd9(df['open'], df['high'], df['low'],
                                           df['close'], df['volume'],
                                           df['bar_size'], df['bar_mid_point'],
                                           df['filled_by'], df['zones'])
    if nsd10:
        temp['nsd10'] = supply_demand._nsd10(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd11:
        temp['nsd11'] = supply_demand._nsd11(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd12:
        temp['nsd12'] = supply_demand._nsd12(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd13:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd13'] = supply_demand._nsd13(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'],
                                             df['bar_mid_point'],
                                             df['filled_by'], df['zones'])
    if nsd14:
        temp['nsd14'] = supply_demand._nsd14(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd15:
        temp['nsd15'] = supply_demand._nsd15(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd16:
        temp['nsd16'] = supply_demand._nsd16(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd17:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd17'] = supply_demand._nsd17(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'],
                                             df['bar_mid_point'],
                                             df['filled_by'], df['zones'])
    if nsd18:
        temp['nsd18'] = supply_demand._nsd18(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd19:
        temp['nsd19'] = supply_demand._nsd19(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['filled_by'], df['zones'])
    if nsd20:
        temp['nsd20'] = supply_demand._nsd20(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd21:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd21'] = supply_demand._nsd21(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'],
                                             df['bar_mid_point'],
                                             df['filled_by'], df['zones'])
    if nsd22:
        temp['nsd22'] = supply_demand._nsd22(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd23:
        temp['nsd23'] = supply_demand._nsd23(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['filled_by'], df['zones'])
    if nsd24:
        temp['nsd24'] = supply_demand._nsd24(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd25:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd25'] = supply_demand._nsd25(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'],
                                             df['bar_mid_point'],
                                             df['filled_by'], df['zones'])
    if nsd26:
        temp['nsd26'] = supply_demand._nsd26(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd27:
        temp['nsd27'] = supply_demand._nsd27(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['filled_by'], df['zones'])
    if nsd28:
        temp['nsd28'] = supply_demand._nsd28(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    if nsd29:
        assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
        temp['nsd29'] = supply_demand._nsd29(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'],
                                             df['bar_mid_point'],
                                             df['filled_by'], df['zones'])
    if nsd30:
        temp['nsd30'] = supply_demand._nsd30(df['open'], df['high'], df['low'],
                                             df['close'], df['volume'],
                                             df['bar_size'], df['filled_by'],
                                             df['zones'])
    df['supply_demand'] = temp.sum(axis=1)


def calculate_effort(df, effort1=True, effort2=True,
                     effort3=True, effort4=True, effort5=True,
                     *args, **kwds):
    assert 'open' in df, 'DataFrame must have open column'
    assert 'high' in df, 'DataFrame must have high column'
    assert 'low' in df, 'DataFrame must have low column'
    assert 'close' in df, 'DataFrame must have close column'
    assert 'volume' in df, 'DataFrame must have volumme column'
    assert 'volume_average' in df, 'DataFrame must have volumme average column'
    assert 'bar_size' in df, 'DataFrame must have bar size column'
    assert 'bar_mid_point' in df, 'DataFrame must have bar mid point column'
    assert 'wrb' in df, 'DataFrame must have wrb column'

    temp_df = pd.DataFrame(index=df.index)
    if effort1:
        temp_df['effort1'] = effort.eff1(df['open'], df['high'], df['low'],
                                         df['close'], df['volume'],
                                         df['volume_average'], df['bar_size'],
                                         df['bar_mid_point'], df['wrb'])
    if effort2:
        temp_df['effort2'] = effort.eff2(df['open'], df['high'], df['low'],
                                         df['close'], df['volume'],
                                         df['volume_average'], df['bar_size'],
                                         df['bar_mid_point'], df['wrb'])
    if effort3:
        temp_df['effort3'] = effort.eff3(df['open'], df['high'], df['low'],
                                         df['close'], df['volume'],
                                         df['volume_average'], df['bar_size'],
                                         df['bar_mid_point'], df['wrb'])
    if effort4:
        temp_df['effort4'] = effort.eff4(df['open'], df['high'], df['low'],
                                         df['close'], df['volume'],
                                         df['volume_average'], df['bar_size'],
                                         df['bar_mid_point'], df['wrb'])
    if effort5:
        temp_df['effort5'] = effort.eff5(df['open'], df['high'], df['low'],
                                         df['close'], df['volume'],
                                         df['volume_average'], df['bar_size'],
                                         df['bar_mid_point'], df['wrb'])
    df['effort'] = temp_df.sum(axis=1)


def calculate_all(df):
    calculate_supply_demand(df)
    calculate_effort(df)
