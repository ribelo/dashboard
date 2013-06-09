#-*- coding: utf-8-*-
import tulip
from app.config import *
from app import market
from app import quantum

store = market.mtgox.store.QuotesStore()

try:
    print('run')
    store.auto_update()
    loop = tulip.get_event_loop()
    loop.run_forever()
except KeyboardInterrupt:
    print('exit')
