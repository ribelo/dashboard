#-*- coding: utf-8-*-
import os
from datetime import datetime, timedelta
import pandas as pd
from . import api
import lzma
import struct
from server.config import DUKASCOPY_QUOTES_PATH


def parse_bi5(bi5, last_date, point=5):
    lzma_ = lzma.LZMADecompressor()
    i, o, h, l, c, v = [], [], [], [], [], []
    s = struct.Struct('>L')
    content = lzma_.decompress(bi5)
    size = len(content)
    idx = 0
    while idx < size:
        time_delta = s.unpack(content[idx:idx + 4])[0]
        price_open = s.unpack(content[idx + 4:idx + 8])[0] / 10 ** point
        price_high = s.unpack(content[idx + 8:idx + 12])[0] / 10 ** point
        price_low = s.unpack(content[idx + 12:idx + 16])[0] / 10 ** point
        price_close = s.unpack(content[idx + 16:idx + 20])[0] / 10 ** point
        volume = s.unpack(content[idx + 20:idx + 24])[0]
        tick = last_date + timedelta(seconds=time_delta)

        i.append(tick)
        o.append(price_open)
        h.append(price_high)
        l.append(price_low)
        c.append(price_close)
        v.append(volume)

        idx += 24
    return pd.DataFrame(data={'open': o, 'high': h, 'low': l,
                              'close': c, 'volume': v}, index=i)


def request_quote(from_date, currency):
    output = pd.DataFrame()
    while True:
        print("DukasCopy Download", str(from_date))
        bi5 = api.request_bi5(from_date, currency)
        try:
            df = parse_bi5(bi5, from_date)
        except lzma.LZMAError as e:
            print(e)
            break
        try:
            output = output.append(df)
        except Exception as e:
            raise(e)
        from_date += timedelta(days=1)
        if from_date >= datetime.utcnow() - timedelta(days=1):
            break
    return output


def save_quote(quotes, currency,):
    if not os.path.exists(DUKASCOPY_QUOTES_PATH):
        os.makedirs(DUKASCOPY_QUOTES_PATH)
    try:
        quotes.save(DUKASCOPY_QUOTES_PATH +
                    '/{}.dat'.format(currency))
    except Exception as e:
        print(e)


def load_quote(currency):
    try:
        return pd.load(DUKASCOPY_QUOTES_PATH +
                       '/{}.dat'.format(currency))
    except FileNotFoundError as e:
        print(e)
        return None
    except Exception as e:
        raise(e)


def clean_quote(quotes, since):
    return quotes[quotes.index >= since]
