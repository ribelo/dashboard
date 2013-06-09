#-*- coding: utf-8-*-
import requests
from app.config import DUKASCOPY_URL


def request_bi5(date, cross, price='BID'):
    url = DUKASCOPY_URL.format(cross=cross, year=date.year,
                               month=date.month - 1, day=date.day,
                               price=price)
    bi5 = requests.get(url)
    return bi5.content
