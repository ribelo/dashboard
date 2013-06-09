#-*- coding: utf-8-*-
import os
from datetime import datetime, timedelta
import csv
import pandas as pd
from . import api
from app.config import NETFOUNDS_QUOTES_PATH


def request_quote(from_date, currency):
    bid, vol, index = [], [], []
    while True:
        print("NetFounds Download", str(from_date))
        csv_data = api.request_csv(from_date, currency)
        if csv_data:
            csv_reader = csv.DictReader(csv_data,
                                        fieldnames=['time', 'bid',
                                        'bid_depth', 'bid_depth_total',
                                        'offer', 'offer_depth',
                                        'offer_depth_total'])
            next(csv_reader)
            for line in csv_reader:
                index.append(datetime.strptime(line['time'], '%Y%m%dT%H%M%S'))
                bid.append(float(line['bid']))
        from_date += timedelta(days=1)
        if from_date >= datetime.utcnow():
            break
    [vol.append(1) for elem in index]
    return pd.DataFrame(data={'bid': bid, 'vol': vol}, index=index)


def save_quote(quotes, currency, path=NETFOUNDS_QUOTES_PATH):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        quotes.save(path + '/{}.dat'.format(currency))
    except Exception as e:
        print(e)


def load_quote(currency, path=NETFOUNDS_QUOTES_PATH):
    try:
        return pd.load(path + '/{}.dat'.format(currency))
    except FileNotFoundError:
        return None
    except Exception as e:
        raise(e)


def clean_quote(quotes, since):
    return quotes[quotes.index >= since]
