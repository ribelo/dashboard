from datetime import datetime, timedelta
import importlib
import pickle

from app import config
from app.redis.redis_db import RED_DB, redis
# from app.quantum import analysis


class MarketStore:

    def __init__(self, market_name, currency, *args, **kwds):
        self.market_name = market_name
        self.market = importlib.import_module(
            'app.market.{}'.format(market_name.lower()))
        self.currency = currency
        self.days_download = getattr(config, (market_name +
                                              '_DAYS_DOWNLOAD').upper())
        self.interval = getattr(config, (market_name + '_INTERVAL').upper())
        self.quotes = {'main': None, 'sister': None}

    def auto_update(self):
        while True:
            self.update_quote()
            self.resample_quote()
            self.dump_db()

    def get_last_index(self):
        try:
            idx = self.load_quote('base').index[-1]
        except AttributeError as e:
            raise e
        else:
            return idx

    def update_quote(self):
        try:
            self.quotes = self.load_quote('base')
        except KeyError as e:
            pass
        try:
            last_date = self.get_last_index()
        except AttributeError:
            last_date = datetime.utcnow() - timedelta(days=self.days_download)
        except Exception:
            raise
        print(last_date)
        quotes = self.market.io.request_quote(
            last_date, currency=self.currency)
        if self.quotes is not None:
            self.quotes = self.quotes.append(quotes)
        else:
            self.quotes = quotes
        self.quotes = self.quotes.sort_index()
        self.save_quote(self.quotes, 'base')

    def resample_quote(self, timeframes=config.QUOTES_TIMEFRAMES):
        quotes = self.load_quote('base')
        for tf in config.QUOTES_TIMEFRAMES:
            resempled_quotes = self.market.io.resample_quote(quotes, tf)
            self.save_quote(resempled_quotes, tf)

    # def analyse_quote(self, indicator=config.QUANTUM_ANALYSE):
    #    pass
    #     for analyse in indicator:
    #         module = getattr(analysis, analyse)
    #         for elem in config.QUANTUM_ANALYSE[analyse]:
    #             indicator = getattr(module, elem)
    #             for tf in config.QUOTES_TIMEFRAMES:
    #                 quotes = self.load_quote(tf)
    #                 indicator(quotes)
    #                 self.save_quote(quotes, tf)

    def save_quote(self, quotes, name):
        try:
            RED_DB.hset('{}_{}'.format(
                self.market_name, self.currency).upper(), name,
                pickle.dumps(quotes))
        except redis.ConnectionError as e:
            print(e)

    def load_quote(self, name):
        quotes = RED_DB.hget('{}_{}'.format(
            self.market_name, self.currency).upper(), name)
        if quotes:
            return pickle.loads(quotes)
        else:
            raise KeyError

    def dump_db(self):
        return RED_DB.bgsave()

    # def clean_quote(self, since):
    #     self.quotes = self.market.io.clean_quote(self.quotes, since)
    #     self.save_quote()
