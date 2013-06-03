#-*- coding: utf-8-*-
import base64
import hashlib
import hmac
import time

from . import config
import requests
import urllib.parse


def urlJoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return '/'.join([arg.strip('/') for arg in args])


class MtGoxError(Exception):
    """Handle MtGoxErrors"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def _specify(name, currency, data=None):
    currency = currency.upper()
    path = urlJoin(currency, 'money', name)
    return _json_request(path, data)


def _get_signature(data):
    assert config.key, "Key not found"
    assert config.secret, "Secret not found"
    h = hmac.new(base64.b64decode(config.secret), data, hashlib.sha512)
    return base64.b64encode(h.digest())


def _json_request(path, data=None):
    do_times = 0
    while True:
        do_times += 1
        #logger.info('Request:', path)
        req = _request(path, data)
        if req.status_code == requests.codes.ok:
            #logger.info('Request: success')
            break
        elif do_times > 10:
            #logger.error('Request: Faild after 10 attempts. ERROR', req.status_code)
            raise Exception(req.status_code)

    jdata = req.json()
    if jdata['result'] == 'success':
        return jdata['data']
    else:
        raise MtGoxError(jdata['error'])


def _request(path, data):
    if data is None:
        data = {'nonce': time.time()}
    else:
        data.update({'nonce': time.time()})
    hash_data = (path + chr(0) + urllib.parse.urlencode(data)).encode('utf-8')
    url = urlJoin(config.url, path)

    signature = _get_signature(hash_data)
    headers = {'Rest-Key': config.key, 'Rest-Sign': signature}

    while True:
        try:
            request = requests.post(url, data=data, headers=headers)
            break
        except ConnectionError:
            pass
        except Exception as e:
            raise e

    return request


def info(currency=config.currency):
    """This method provides a lot of information about your account

    return:
    {
        "data": {
            "Created": "yyyy-mm-dd hh:mm:ss",print('sex')
            "Id": "abc123",
            "Index": "123",
            "Language": "en_US",
            "Last_Login": "yyyy-mm-dd hh:mm:ss",
            "Login": "username",
            "Monthly_Volume":                   **Currency Object**,
            "Trade_Fee": 0.6,
            "Rights": ['deposit', 'get_info', 'merchant', 'trade', 'withdraw'],
            "Wallets": {
                "BTC": {
                    "Balance":                  **Currency Object**,
                    "Daily_Withdraw_Limit":     **Currency Object**,
                    "Max_Withdraw":             **Currency Object**,
                    "Monthly_Withdraw_Limit": null,
                    "Open_Orders":              **Currency Object**,
                    "Operations": 1,
                },
                "USD": {
                    "Balance":                  **Currency Object**,
                    "Daily_Withdraw_Limit":     **Currency Object**,
                    "Max_Withdraw":             **Currency Object**,
                    "Monthly_Withdraw_Limit":   **Currency Object**,
                    "Open_Orders":              **Currency Object**,
                    "Operations": 0,
                },
                "JPY":{...}, "EUR":{...},
                // etc, depends what wallets you have
            },
        },
        "result": "success"
    }

    """
    return _specify(name='info', currency=currency)


def orders(currency=config.currency):
    """Get information on your current orders

    return:
    {
        "oid": "abc123-def456-..",
        "currency": "USD",
        "item": "BTC",
        "type": "bid",
        "amount":           **Currency Object**,
        "effective_amount": **Currency Object**,
        "price":            **Currency Object**,
        "status": "pending",
        "date": 1365517594,
        "priority": "1365517594817935",
        "actions": []
    }

    """
    return _specify('orders', currency=currency)


def currency(currency=config.currency):
    """Get information for a given currency

    return:
    {
        "result":"success",
        "data": {
            "currency":"USD",
            "name":"Dollar",
            "symbol":"$",
            "decimals":"5",
            "display_decimals":"2",
            "symbol_position":"before",
            "virtual":"N",
            "ticker_channel":"abc123-def456",
            "depth_channel":"abc123-def456"
        }
    }

    """
    data = {'currency': currency}
    return _specify('currency', data=data, currency=currency)


def ticker(currency=config.currency):
    """Get the most recent information for a currency pair

    return:
    {
        "result":"success",
        "data": {
            "high":       **Currency Object - USD**,
            "low":        **Currency Object - USD**,
            "avg":        **Currency Object - USD**,
            "vwap":       **Currency Object - USD**,
            "vol":        **Currency Object - BTC**,
            "last_local": **Currency Object - USD**,
            "last_orig":  **Currency Object - ???**,
            "last_all":   **Currency Object - USD**,
            "last":       **Currency Object - USD**,
            "buy":        **Currency Object - USD**,
            "sell":       **Currency Object - USD**,
            "now":        "1364689759572564"
        }
    }

    """
    return _specify(name='ticker', currency=currency)


def ticker_fast(currency=config.currency):
    """Get the most recent information for a currency pair

    return:
    {
        "result":"success",
        "data": {
            "last_local": **Currency Object - USD**,
            "last":       **Currency Object - USD**,
            "last_orig":  **Currency Object - EUR**,
            "last_all":   **Currency Object - USD**,
            "buy":        **Currency Object - USD**,
            "sell":       **Currency Object - USD**,
            "now":        "1366230242125772"
        }
    }

    """
    return _specify(name='ticker_fast', currency=currency)


def depth_fetch(currency=config.currency):
    """Gets recent depth information

    return:
    {"result":"success","data":{
        "asks":[...],
        "bids":[...],
        "filter_min_price":{"value":"83.48403","value_int":"8348403","display":"$83.48403","display_short":"$83.48","currency":"USD"},
        "filter_max_price":{"value":"102.03603","value_int":"10203603","display":"$102.03603","display_short":"$102.04","currency":"USD"}
    }}

    """
    return _specify(name='depth/fetch', currency=currency)


def depth_full(currency=config.currency):
    """Gets a complete full depth data

    return:
    {"result":"success","data":{
        "asks":[
            {"price":93.06545,"amount":0.07284541,"price_int":"9306545","amount_int":"7284541","stamp":"1364769641591046"},
            {"price":93.06546,"amount":0.81618662,"price_int":"9306546","amount_int":"81618662","stamp":"1364769116973406"},
            {"price":93.4,"amount":0.02,"price_int":"9340000","amount_int":"2000000","stamp":"1364769080120861"},
            ...
        ],
        "bids":[
            {"price":1.0e-5,"amount":30694957.01,"price_int":"1","amount_int":"3069495700999999","stamp":"1364764907440546"},
            {"price":2.0e-5,"amount":10000.02,"price_int":"2","amount_int":"1000002000000","stamp":"1364418775588024"},
            {"price":3.0e-5,"amount":41515.8015,"price_int":"3","amount_int":"4151580150000","stamp":"1364225564960621"},
            ...
        ]
    }}

    """
    return _specify(name='depth/full')


def wallet_history(currency=config.currency):
    """
    Gets the transaction history of a specified currency
    wallet.

    return:
    {
        "result": "success",
        "data": {
            "records": "17",
            "result": [
                {
                    "Index": "17",
                    "Date": 1366243097,
                    "Type": "out",
                    "Value":   **Currency Object**,
                    "Balance": **Currency Object**,
                    "Info": "BTC sold: [tid:1366243097811202] 0.25000000 BTC at $126.50000",
                    "Link":[
                        "123456789-0abc-def0-1234-567890abcdef",
                        "Money_Trade",
                        "1366243097811202"]
                },
                {
                    "Index": "16",
                    "Date": 1366218001,
                    "Type": "deposit",
                    "Value":   **Currency Object**,
                    "Balance": **Currency Object**,
                    "Info": "1BitcoinAddress789fhjka890jkl",
                    "Link":[
                        "123456789-0abc-def0-1234-567890abcdef",
                        "Money_Bitcoin_Block_Tx_Out",
                        "1BitcoinTransaction780gfsd8970fg:9"]
                },
                {...},
            ],
            "current_page": 1,
            "max_page": 1,
            "max_results": 50
        }
    }

    """
    data = {'currency': currency}
    return _specify('wallet/history', currency=currency, data=data)


def trades_fetch(since=None, currency=config.currency):
    """This method gets up to 1000 trades from the date
    specified (or the most recent, if none)

    The tid after which to retrieve trades. For most trades,
    this is the unix microstamp (see below). This is optinal
    - if omitted, only the most recent 1000 trades will be
    returned.

    return:
    {"result":"success","data":[
        {"date":1364767201,"price":"92.65","amount":"0.47909825","price_int":"9265000","amount_int":"47909825","tid":"1364767201381791","price_currency":"USD","item":"BTC","trade_type":"bid","primary":"Y","properties":"limit"},
        {"date":1364767207,"price":"92.65","amount":"0.01024284","price_int":"9265000","amount_int":"1024284","tid":"1364767207406066","price_currency":"USD","item":"BTC","trade_type":"bid","primary":"Y","properties":"limit"},
        {"date":1364767232,"price":"92.65","amount":"1.25637797","price_int":"9265000","amount_int":"125637797","tid":"1364767232522802","price_currency":"USD","item":"BTC","trade_type":"bid","primary":"Y","properties":"limit"},
        {"date":1364767236,"price":"92.65","amount":"0.01","price_int":"9265000","amount_int":"1000000","tid":"1364767236979043","price_currency":"USD","item":"BTC","trade_type":"bid","primary":"Y","properties":"limit"},
        {"date":1364767245,"price":"92.65","amount":"0.01","price_int":"9265000","amount_int":"1000000","tid":"1364767245879648","price_currency":"USD","item":"BTC","trade_type":"bid","primary":"Y","properties":"limit"}
    ]}

    """
    data = {'since': since}
    return _specify(name='trades/fetch', currency=currency, data=data)


def order_quote(type_, amount, currency=config.currency):
    """Get an up-to-date quote for a bid or ask transaction

    return:
    {"result":"success","data":{"amount":9197999}}
    """
    assert type_ == 'bid' or type_ == 'ask'
    assert isinstance(amount, int)
    data = {'type': type_,
            'amount': amount}
    return _specify('order/quote', data)


def order_add(type_, amount, price, currency=config.currency):
    """Creates a currency trade order

    return:
    {"result":"success","data":"abc123-def45-.."}
    """

    assert type_ == 'bid' or type_ == 'ask'
    assert isinstance(amount, int)
    assert isinstance(price, int)
    data = {'type': type_,
            'amount_int': amount,
            'price_int': price}
    return _specify('order/add', currency=currency, data=data)


def order_lag(currency=config.currency):
    """Returns the lag time for executing orders in microseconds

    return:
    {"result":"success","data":{"lag":2319790,"lag_secs":2.31979,"lag_text":"2.31979 seconds"}}
    """

    return _specify('order/lag', currency=currency)


def _timestamp64to32(timestamp):
    return timestamp * 1e-6


def _timestamp32to64(timestamp):
    return timestamp * 1e6
