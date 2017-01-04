# -*- coding: utf-8 -*-
import json
import logging
import redis
import time

# Redis reserved keys
PRIMITIVE_QUEUE = "PRIM_QUEUE"


def connect_redis(host, port, db):
    """
    Return a Redis object
    """
    val = None
    while val is None:
        try:
            r = redis.StrictRedis(host='127.0.0.1',
                                  port=6379,
                                  db=0)
            val = r.dbsize()
            return r
        except Exception:
            logging.exception("Cannot connect to Redis - Wait 30 seconds")
            time.sleep(30)


class RedisObject(object):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def push_primitive_queue(self, data):
        self.redis_client.rpush(PRIMITIVE_QUEUE, json.dumps(data))

    def pop_primitive_queue(self):
        data = self.redis_client.lpop(PRIMITIVE_QUEUE)
        if data:
            return json.loads(data)
        else:
            return {}
