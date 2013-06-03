#-*- coding: utf-8-*-
import requests


def request_csv(date, currency):
    url = 'http://www.netfonds.no/quotes/posdump.php?date={}&paper={}.FXSB&csv_format=csv'.format(date.strftime('%Y%m%d'), currency)
    data = requests.get(url)
    return data.text.splitlines()
