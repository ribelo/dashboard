#-*- coding: utf-8-*-

QUANTUM_CONTRACTION = 32
QUANTUM_LOOK_BACK = 256

DUKASCOPY_RUN = False
DUKASCOPY_DAYS_DOWNLOAD = 30
DUKASCOPY_INTERVAL = 12
DUKASCOPY_QUOTES_PATH = './app/quotes/DukasCopy/'
DUKASCOPY_URL = 'http://www.dukascopy.com/datafeed/{cross}/{year}/{month:02d}/{day:02d}/{price}_candles_min_1.bi5'

MTGOX_RUN = False
MTGOX_DAYS_DOWNLOAD = 30
MTGOX_INTERVAL = 12
MTGOX_QUOTES_PATH = './app/quotes/MtGox/'
MTGOX_CURRENCY = 'BTCUSD'
MTGOX_URL = 'http://data.mtgox.com/api/2'
MTGOX_KEY = 'a67cb596-8c11-40b1-aaf1-70446c350d50'
MTGOX_SECRET = 'sWsFxJZiiPeNN34d9z+gMeJpiNC5eQm1uMFR7rw/oCUnEHN1p7NEwz2igoSMHhoeppnFE9y7W4U02eJ2e1tjoQ=='

NETFOUNDS_RUN = False
NETFOUNDS_DAYS_DOWNLOAD = 30
NETFOUNDS_INTERVAL = 12
NETFOUNDS_QUOTES_PATH = './app/quotes/NetFounds/'
NETFOUNDS_URL = 'http://www.netfonds.no/quotes/posdump.php?date={}&paper={}.FXSB&csv_format=csv'
