from datetime import datetime, timedelta
import importlib

import arrow
import redis
import tulip

from app import config


class QuotesStore:

    def __init__(self, market_name, currency, *args, **kwds):
        self.market = importlib.import_module(
            'app.market.{}'.format(market_name))
        self.currency = currency
        self.days_download = getattr(config, (market_name +
                                              '_DAYS_DOWNLOAD').upper())
        self.interval = getattr(config, (market_name + '_INTERVAL').upper())
        self.quotes = None

    #@tulip.task
    def auto_update(self):
        while True:
            self.update_quote()
            #yield from tulip.sleep(self.interval)

    #@tulip.coroutine
    def get_last_index(self):
        try:
            idx = self.quotes.index[-1]
        except AttributeError as e:
            raise e
        else:
            return idx

    #@tulip.coroutine
    def update_quote(self):
        try:
            self.load_quote()
        except FileNotFoundError as e:
            pass
        try:
            last_date = self.get_last_index()
        except AttributeError:
            last_date = datetime.utcnow() - timedelta(days=self.days_download)
        except Exception:
            raise
        print(last_date)
        quotes = self.market.io.request_quote(last_date, currency=self.currency)
        if self.quotes is not None:
            self.quotes = self.quotes.append(quotes)
        else:
            self.quotes = quotes
        self.quotes = self.quotes.sort_index()
        self.save_quote()

    #@tulip.coroutine
    def save_quote(self):
        self.market.io.save_quote(quotes=self.quotes, currency=self.currency)

    #@tulip.coroutine
    def load_quote(self):
        self.quotes = self.market.io.load_quote(currency=self.currency)

    #@tulip.coroutine
    def clean_quote(self, since):
        self.quotes = self.market.io.clean_quote(self.quotes, since)
        self.save_quote()

    #@tulip.coroutine
    def parse_quote(self, tf, timezone='CET'):
        return self.market.io.parse_quote(quotes=self.quotes, tf=tf,
                                          timezone=timezone)
