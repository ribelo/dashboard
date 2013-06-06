#-*- coding: utf-8-*-
import requests
from server.config import NETFOUNDS_QUOTES_PATH


def request_csv(date, currency):
    url = NETFOUNDS_QUOTES_PATH.format(date.strftime('%Y%m%d'), currency)
    data = requests.get(url)
    return data.text.splitlines()
