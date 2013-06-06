#-*- coding: utf-8-*-
import os
from datetime import datetime
from operator import itemgetter
import tulip

import pandas as pd
from . import config
from . import api


def _tid_to_datetime(tid):
    return datetime.fromtimestamp(tid * 1e-6)


def _datetime_to_tid(date):
    return date.timestamp() * 1e6


def request_quote(from_date, currency=config.currency):
    from_date = _datetime_to_tid(from_date)

    bid, vol, index = [], [], []
    while True:
        print("MtGox Download", _tid_to_datetime(from_date))
        jdata = api.trades_fetch(since=from_date, currency=currency)
        if jdata:
            for line in sorted(jdata, key=itemgetter('tid')):
                index.append(_tid_to_datetime(int(line['tid'])))
                bid.append(float(line['price']))
                vol.append(float(line['amount']))
        if _tid_to_datetime(from_date) < index[-1]:
            print(_tid_to_datetime(from_date), index[-1])
            from_date = _datetime_to_tid(index[-1])
        else:
            print(_tid_to_datetime(from_date), index[-1])
            break

    return pd.DataFrame(data={'bid': bid, 'vol': vol}, index=index)


def save_quote(quotes, currency=config.currency, path=config.data_path):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        quotes.save(path + '/{}.dat'.format(currency))
    except Exception as e:
        print(e)


def load_quote(currency=config.currency, path=config.data_path):
    try:
        return pd.load(path + '/{}.dat'.format(currency))
    except FileNotFoundError:
        return None
    except Exception as e:
        raise(e)


def clean_quote(quotes, since):
    return quotes[quotes.index >= since]


def parse_quote(quotes, tf, timezone='CET'):
    df = quotes.copy()
    ohlc = df.bid.resample('{}T'.format(tf), how='ohlc', fill_method='pad')
    vol = df.vol.resample('{}T'.format(tf), how='sum', fill_method=None)
    ohlc['volume'] = vol
    return ohlc
