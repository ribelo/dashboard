#-*- coding: utf-8-*-
import os
import struct
import lzma
from datetime import datetime, timedelta
import urllib
import dateutil
import pytz
import json


def get_candle_bi5(cross, date, price='BID'):
    if type(date) == str:
        date = dateutil.parser.parse(date).replace(
            hour=0, minute=0, second=0, microsecond=0)
    url = 'http://www.dukascopy.com/datafeed/{cross}/{year}/{month:02d}/{day:02d}/{price}_candles_min_1.bi5'.format(
        cross=cross, year=date.year, month=date.month - 1, day=date.day, price=price)
    try:
        bi5 = urllib.request.urlretrieve(url)
    except urllib.request.HTTPError:
        print('Problem with url:', url)
        raise

    return bi5


def get_ticks_bi5(cross, date, price='BID'):
    if type(date) == str:
        date = dateutil.parser.parse(date).replace(
            hour=0, minute=0, second=0, microsecond=0)
    url = 'http://www.dukascopy.com/datafeed/{cross}/{year}/{month:02d}/{day:02d}/{hour:02d}h_ticks.bi5'.format(
        cross=cross, year=date.year, month=date.month - 1, day=date.day, hour=date.hour + 1)
    try:
        bi5 = urllib.request.urlretrieve(url)
    except urllib.request.HTTPError:
        raise

    return bi5


def parse_candle(bi5, date, point=5):
    quote = {}
    if type(date) == str:
        date = dateutil.parser.parse(date).replace(
            tzinfo=pytz.utc, hour=0, minute=0, second=0, microsecond=0)
    s = struct.Struct('>L')
    try:
        with lzma.open(bi5[0]) as f:
            content = f.read()
    except EOFError:
        print('{}: File is not valid lzma file. Conitnue'.format(date))
        return quote
    size = len(content)
    idx = 0
    while idx < size:
        time_delta = s.unpack(content[idx:idx + 4])[0]
        price_open = s.unpack(content[idx + 4:idx + 8])[0] / 10 ** point
        price_high = s.unpack(content[idx + 8:idx + 12])[0] / 10 ** point
        price_low = s.unpack(content[idx + 12:idx + 16])[0] / 10 ** point
        price_close = s.unpack(content[idx + 16:idx + 20])[0] / 10 ** point
        volume = s.unpack(content[idx + 20:idx + 24])[0]
        last_candle = date.astimezone(pytz.utc) + timedelta(seconds=time_delta)
        try:
            quote[last_candle]
        except KeyError:
            quote[last_candle] = {}
        finally:
            quote[last_candle] = {'open': price_open, 'high': price_high,
                                  'low': price_low, 'close': price_close, 'vol': volume}
        idx += 24
    return quote


def parse_ticks(bi5, date, point=5):
    quote = {}
    s = struct.Struct('>L')
    try:
        with lzma.open(bi5[0]) as f:
            content = f.read()
    except EOFError:
        print('{}: File is not valid lzma file. Conitnue'.format(date))
        return quote
    size = len(content)
    idx = 0
    if type(date) == str:
        date = dateutil.parser.parse(date).replace(
            tzinfo=pytz.utc, hour=0, minute=0, second=0, microsecond=0)
    last_candle = date
    last_time = last_candle
    price_open, price_high, price_low, price_close, volume = 0, float(
        '-inf'), float('inf'), 0, 0
    while idx < size:
        time_delta = s.unpack(content[idx:idx + 4])[0]
        # ask = s.unpack(content[idx + 4:idx + 8])[0] / 10 ** point
        bid = s.unpack(content[idx + 8:idx + 12])[0] / 10 ** point
        # ask_vol = s.unpack(content[idx + 12:idx + 16])[0] / 10 ** point
        bid_vol = s.unpack(content[idx + 16:idx + 20])[0] / 10 ** point
        last_time = date.astimezone(pytz.utc) + timedelta(milliseconds=time_delta)
        if price_open == 0:
            price_open = bid
        if bid > price_high:
            price_high = bid
        if bid < price_low:
            price_low = bid
        price_close = bid
        volume += bid_vol
        if (last_time - last_candle).seconds >= 60:
            try:
                quote[last_candle]
            except KeyError:
                quote[last_candle] = {}
            finally:
                quote[last_candle] = {'open': price_open, 'high':
                                      price_high, 'low': price_low, 'close': price_close, 'vol': volume}
            # price_open, price_high, price_low, price_close, volume = 0,
            # float('-inf'), float('inf'), 0, 0
            price_open, price_high, price_low, price_close, volume = price_close, price_close, price_close, price_close, 0
            last_candle += timedelta(seconds=60)

        idx += 20
    return quote


def download_csv(cross, from_date, to_date, path):
    date = min([from_date, to_date])
    utcnow = datetime.utcnow()
    while date.date() < to_date.date():
        if not _csv_exist(cross, date, path):
            if date.date() < utcnow.date():
                bi5 = _get_candle_bi5(cross, date)
                quote = _parse_candle(bi5, date)
                _save_quote(quote, cross, date, path)
            else:
                bi5 = _get_ticks_bi5(cross, date)
                quote = _parse_ticks(bi5, date)
                _save_quote(quote, cross, date, path)
        date += timedelta(days=1)
