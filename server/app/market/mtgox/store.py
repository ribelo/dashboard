#-*- coding: utf-8-*-
from datetime import datetime, timedelta
import pickle
import time
import uuid

from . import api
from . import io
import arrow
import redis
import tulip

from app.config import *


class QuotesStore:

    def __init__(self, *args, **kwds):
        self.interval = MTGOX_INTERVAL
        self.quotes = None
        self.currency = MTGOX_CURRENCY
        self.days_download = MTGOX_DAYS_DOWNLOAD

    @tulip.task
    def auto_update(self):
        while True:
            yield from self.update_quote()
            yield from tulip.sleep(self.interval)

    @tulip.coroutine
    def _get_last_date(self):
        from_day = datetime.utcnow() - timedelta(days=self.days_download)
        if self.quotes is not None:
            date = max(from_day, self.quotes.index[-1])
        else:
            date = from_day
        return date

    @tulip.coroutine
    def _seve_last_tid(self):
        redis.hset('mtgox', 'last_date', self._get_last_date())

    @tulip.coroutine
    def update_quote(self, interval=1):
        if self.quotes is None:
            yield from self.load_quote()
        print(self.quotes)
        last_date = yield from self._get_last_date()
        quotes = io.request_quote(last_date)
        if self.quotes is not None:
            self.quotes = self.quotes.append(quotes)
        else:
            self.quotes = quotes
        self.quotes = self.quotes.sort_index()
        yield from self.save_quote()

    @tulip.coroutine
    def save_quote(self):
        io.save_quote(quotes=self.quotes, currency=self.currency)

    @tulip.coroutine
    def load_quote(self):
        self.quotes = io.load_quote(currency=self.currency)

    @tulip.coroutine
    def clean_quote(self, since):
        self.quotes = io.clean_quote(self.quotes, since)
        self.save_quote()

    @tulip.coroutine
    def parse_quote(self, tf, timezone='CET'):
        return io.parse_quote(quotes=self.quotes, tf=tf, timezone=timezone)


class MarketStore:

    def __init__(self, currency=None, redis_=None, db_nr=0, *args, **kwds):
        self.redis = redis_ if redis_ else redis.StrictRedis(db=db_nr)
        self.db_nr = db_nr
        self.currency = MTGOX_CURRENCY if not currency else currency
        self.tasks = [
            self.update_lag, self.update_ticker_fast, self.update_info]

    @tulip.task
    def run(self):
        while True:
            for task in self.tasks:
                yield from task()
            yield from tulip.sleep(1)

    @tulip.coroutine
    def update_lag(self):
        self.redis.hset('mtgox', 'lag', pickle.dumps(api.order_lag()))

    @tulip.coroutine
    def update_ticker(self):
        self.redis.hset('mtgox', 'ticker', pickle.dumps(api.ticker()))

    @tulip.coroutine
    def update_ticker_fast(self):
        self.redis.hset('mtgox', 'ticker_fast', pickle.dumps(
            api.ticker_fast()))

    @tulip.coroutine
    def update_info(self):
        self.redis.hset('mtgox', 'info', pickle.dumps(api.info()))

    @tulip.coroutine
    def update_currency(self):
        self.redis.hset('mtgox', 'currency', pickle.dumps(api.currency()))

    @tulip.coroutine
    def update_orders(self):
        self.redis.hset('mtgox', 'orders', pickle.dumps(api.orders()))

    @tulip.coroutine
    def update_depth_fetch(self):
        self.redis.hset('mtgox', 'depth_fetch', pickle.dumps(
            api.depth_fetch()))

    @tulip.coroutine
    def update_depth_full(self):
        self.redis.hset('mtgox', 'depth', pickle.dumps(api.depth_full()))

    @tulip.coroutine
    def update_wallet_history(self):
        self.redis.hset('mtgox', 'depth', pickle.dumps(api.wallet_history()))


class Watchman:

    def __init__(self, redis_=None, db_nr=0):
        self.redis = redis_ if redis_ else redis.StrictRedis(db=db_nr)

    @tulip.task
    def watch(self):
        while True:
            for order_ in reversed(self.redis.lrange('orders', 0, -1)):
                order = pickle.loads(order_)
                print('order', order)
                if order['type'] == 'buy':
                    self.redis.lrem(name='orders', count=0, value=order_)
                    if order['take']:
                        assert order['price'] < order['take']
                    if order['stop']:
                        assert order['price'] < order['stop']
                    yield from self.buy_market(currency=order['currency'],
                                               amount=order['amount'],
                                               stop=order['stop'],
                                               take=order['take'])
                    if order['stop']:
                        yield from self.sell_limit(currency=order['currency'],
                                                   amount=order['amount'],
                                                   price=order['stop'],
                                                   stop=0,
                                                   take=0)
                    if order['take']:
                        yield from self.sell_stop(currency=order['currency'],
                                                  amount=order['amount'],
                                                  price=order['take'],
                                                  stop=0,
                                                  take=0)
                elif order['type'] == 'buy_stop':
                    if order['take']:
                        assert order['price'] < order['take']
                    if order['stop']:
                        assert order['price'] > order['stop']
                    trigger = yield from self.check_buy_stop(order=order)
                    if trigger:
                        self.redis.lrem(name='orders', count=0, value=order_)
                        yield from self.buy_market(currency=order['currency'],
                                                   amount=order['amount'],
                                                   stop=order['stop'],
                                                   take=order['take'])

                elif order['type'] == 'buy_limit':
                    if order['take']:
                        assert order['price'] < order['take']
                    if order['stop']:
                        assert order['price'] > order['stop']
                    trigger = yield from self.check_buy_limit(order=order)
                    if trigger:
                        self.redis.lrem(name='orders', count=0, value=order_)
                        yield from self.buy_market(currency=order['currency'],
                                                   amount=order['amount'],
                                                   stop=order['stop'],
                                                   take=order['take'])

                elif order['type'] == 'sell':
                    self.redis.lrem(name='orders', count=0, value=order_)
                    if order['take']:
                        assert order['price'] > order['take']
                    if order['stop']:
                        assert order['price'] < order['stop']
                    yield from self.sell_market(currency=order['currency'],
                                                amount=order['amount'],
                                                stop=order['stop'],
                                                take=order['take'])
                    if order['stop']:
                        yield from self.buy_limit(currency=order['currency'],
                                                  amount=order['amount'],
                                                  price=order['take'],
                                                  stop=0,
                                                  take=0)
                    if order['take']:
                        yield from self.buy_stop(currency=order['currency'],
                                                 amount=order['amount'],
                                                 price=order['stop'],
                                                 stop=0,
                                                 take=0)

                elif order['type'] == 'sell_stop':
                    if order['take']:
                        assert order['price'] > order['take']
                    if order['stop']:
                        assert order['price'] < order['stop']
                    trigger = yield from self.check_sell_stop(order=order)
                    if trigger:
                        self.redis.lrem(name='orders', count=0, value=order_)
                        yield from self.buy_market(currency=order['currency'],
                                                   amount=order['amount'],
                                                   stop=order['stop'],
                                                   take=order['take'])

                elif order['type'] == 'sell_limit':
                    if order['take']:
                        assert order['price'] > order['take']
                    if order['stop']:
                        assert order['price'] < order['stop']
                    trigger = yield from self.check_sell_limit(order=order)
                    if trigger:
                        self.redis.lrem(name='orders', count=0, value=order_)
                        yield from self.buy_market(currency=order['currency'],
                                                   amount=order['amount'],
                                                   stop=order['stop'],
                                                   take=order['take'])

            yield from tulip.sleep(1)

    @tulip.coroutine
    def buy_market(self, currency, amount, stop, take):
        # api.order_quote('bid', amount, currency)
        print('buy_market')
        if stop:
            self.sell_stop(currency, amount, stop, 0, 0)
        if take:
            self.sell_limit(currency, amount, take, 0, 0)

    @tulip.coroutine
    def buy_stop(self, currency, amount, price, stop, take):
        ticket = uuid.uuid4().hex
        order = pickle.dumps({'ticket': ticket, 'currency': currency,
                             'type': 'buy_stop', 'amount': amount,
                             'price': price, 'stop': stop, 'take': take})
        self.redis.rpush('orders', order)

    @tulip.coroutine
    def check_buy_stop(self, order):
        ticker = pickle.loads(self.redis.hget('mtgox', 'ticker_fast'))
        ticker_price = int(ticker['buy']['value_int'])
        print('check buy stop, ticker:', ticker_price, 'price', order['price'])
        if order['price'] > ticker_price:
            return True
        else:
            return False

    @tulip.coroutine
    def buy_limit(self, currency, amount, price, stop, take):
        ticket = uuid.uuid4().hex
        order = pickle.dumps({'ticket': ticket, 'currency': currency,
                             'type': 'buy_limit', 'amount': amount,
                             'price': price, 'stop': stop, 'take': take})
        self.redis.rpush('orders', order)

    @tulip.coroutine
    def check_buy_limit(self, order):
        ticker = pickle.loads(self.redis.hget('mtgox', 'ticker_fast'))
        ticker_price = int(ticker['buy']['value_int'])
        print('check buy limit, ticker:',
              ticker_price, 'price', order['price'])
        if order['price'] < ticker_price:
            return True
        else:
            return False

    @tulip.coroutine
    def sell_market(self, currency, amount, stop, take):
        # api.order_quote('ask', amount, currency)
        print('sell_market')
        if stop:
            self.buy_stop(currency, amount, stop, 0, 0)
        if take:
            self.buy_limit(currency, amount, take, 0, 0)

    @tulip.coroutine
    def sell_stop(self, currency, amount, price, stop, take):
        ticket = uuid.uuid4().hex
        order = pickle.dumps({'ticket': ticket, 'currency': currency,
                             'type': 'sell_stop', 'amount': amount,
                             'price': price, 'stop': stop, 'take': take})
        self.redis.rpush('orders', order)

    @tulip.coroutine
    def check_sell_stop(self, order):
        ticker = pickle.loads(self.redis.hget('mtgox', 'ticker_fast'))
        ticker_price = int(ticker['sell']['value_int'])
        print('check sell stop, ticker:',
              ticker_price, 'price', order['price'])
        if order['price'] < ticker_price:
            return True
        else:
            return False

    @tulip.coroutine
    def sell_limit(self, currency, amount, price, stop, take):
        ticket = uuid.uuid4().hex
        order = pickle.dumps({'ticket': ticket, 'currency': currency,
                             'type': 'sell_limit', 'amount': amount,
                             'price': price, 'stop': stop, 'take': take})
        self.redis.rpush('orders', order)

    @tulip.coroutine
    def check_sell_limit(self, order):
        ticker = pickle.loads(self.redis.hget('mtgox', 'ticker_fast'))
        ticker_price = int(ticker['sell']['value_int'])
        print('check sell limit, ticker:',
              ticker_price, 'price', order['price'])
        if order['price'] > ticker_price:
            return True
        else:
            return False
