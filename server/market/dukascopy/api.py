#-*- coding: utf-8-*-
import requests


def request_bi5(date, cross, price='BID'):
    url = 'http://www.dukascopy.com/datafeed/{cross}/{year}/{month:02d}/{day:02d}/{price}_candles_min_1.bi5'.format(
        cross=cross, year=date.year, month=date.month - 1, day=date.day, price=price)
    bi5 = requests.get(url)
    return bi5.content

