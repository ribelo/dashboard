#-*- coding: utf-8-*-

CONTRACTION = 32
LOOK_BACK = 256

MARKET = {
    'DukasCopy': {
        'DAYS_DOWNLAOD': 30,
        'INTERVAL': 12,
        'QUOTES_PATH': './quotes/NetFounds/',
        'URL': 'http://www.netfonds.no/quotes/posdump.php?date={}&paper={}.FXSB&csv_format=csv'
    },
    'MtGox': {
        'DAYS_DOWNLAOD': 30,
        'INTERVAL': 12,
        'KEY': 'a67cb596-8c11-40b1-aaf1-70446c350d50',
        'QUOTES_PATH': './quotes/MtGox/',
        'SECRET': 'sWsFxJZiiPeNN34d9z+gMeJpiNC5eQm1uMFR7rw/oCUnEHN1p7NEwz2igoSMHhoeppnFE9y7W4U02eJ2e1tjoQ==',
        'URL': 'http://data.mtgox.com/api/2'
    },
    'NetFounds': {
        'DAYS_DOWNLAOD': 30,
        'INTERVAL': 12,
        'QUOTES_PATH': './quotes/NetFounds/',
        'URL': 'http://www.netfonds.no/quotes/posdump.php?date={}&paper={}.FXSB&csv_format=csv'
    }
}
