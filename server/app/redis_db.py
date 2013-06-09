#-*- coding: utf-8-*-

import redis

RED_DB = redis.StrictRedis()
try:
    RED_DB.ping()
except redis.ConnectionError as e:
    print(e)
