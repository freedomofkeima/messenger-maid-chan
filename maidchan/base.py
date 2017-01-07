# -*- coding: utf-8 -*-
import json
import logging
import redis
import time

# Redis reserved keys
USER = "USER"
USERS = "USERS"
PRIMITIVE_QUEUE = "PRIM_QUEUE"
ACTIVE_QUESTION = "ACTIVE_QUESTION"
SCHEDULES = "SCHEDULES"


def connect_redis(host, port, db):
    """
    Return a Redis object
    """
    val = None
    while val is None:
        try:
            r = redis.StrictRedis(host=host,
                                  port=port,
                                  db=db)
            val = r.dbsize()
            return r
        except Exception:
            logging.exception("Cannot connect to Redis - Wait 30 seconds")
            time.sleep(30)


class RedisDriver(object):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def set_users(self, data):
        """
        data: list of recipient_id which has talked at least once
        e.g.: ["1242484182465008", "1242484182465009", "1242484182465007"]
        """
        users = {
            "users": data
        }
        self.redis_client.set(USERS, json.dumps(users))

    def get_users(self):
        data = self.redis_client.get(USERS)
        if data:
            return json.loads(data).get("users", [])
        else:
            return []

    def set_user(self, recipient_id, data):
        """
        data: dict of all user's information
        e.g.: {
                  "nickname": "Ryuunosuke",
                  "offerings_status": "subscribed",
                  "japanese_status": "subscribed",
                  "morning_time": "09:00",
                  "night_time": "23:00",
                  "kanji_level": "N3"
              }
        """
        redis_key = "{}_{}".format(USER, recipient_id)
        self.redis_client.set(redis_key, json.dumps(data))

    def get_user(self, recipient_id):
        data = self.redis_client.get(recipient_id)
        if data:
            return json.loads(data)
        else:
            return {}

    def push_primitive_queue(self, data):
        """
        data: message in dict for primitive image filtering jobs
        e.g.: {
                  "url": "...",  # Facebook URL
                  "recipient_id": "1242484182465008"
              }
        """
        self.redis_client.rpush(PRIMITIVE_QUEUE, json.dumps(data))

    def pop_primitive_queue(self):
        data = self.redis_client.lpop(PRIMITIVE_QUEUE)
        if data:
            return json.loads(data)
        else:
            return {}

    def set_active_question(self, recipient_id, question_type):
        """
        Store last asked question type from Maid-chan for
        the specified recipient_id.
        Particularly useful to decide the next Maid-chan's response
        """
        redis_key = "{}_{}".format(ACTIVE_QUESTION, recipient_id)
        self.redis_client.set(redis_key, question_type)

    def get_active_question(self, recipient_id):
        redis_key = "{}_{}".format(ACTIVE_QUESTION, recipient_id)
        data = self.redis_client.get(redis_key)
        if data:
            self.redis_client.delete(redis_key)
            return int(data)
        else:
            return -1

    def set_schedules(self, data):
        """
        data: dict of all scheduled activities and all daily choices
        e.g.: {
                  "schedules": [
                      {
                          "recipient_id": "1242484182465008",
                          "type": "morning_offering",
                          "next_mt": "..."
                      }
                  ],
                  "metadata": {
                      "morning_offering_text": "normal_1",
                      "morning_offering_image": "example.png",
                      "night_offering_text": "special_1",
                      "night_offering_image": "example2.png",
                      "kanji_n1": "",
                      "kanji_n2": "",
                      "kanji_n3": "",
                      "kanji_n4": "",
                      "vocabulary": "",
                      "next_mt": "..."
                  }
              }
        """
        self.redis_client.set(SCHEDULES, json.dumps(data))

    def get_schedules(self):
        data = self.redis_client.get(SCHEDULES)
        if data:
            return json.loads(data)
        else:
            return {}
