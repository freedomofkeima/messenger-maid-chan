# -*- coding: utf-8 -*-
import time
from maidchan.base import connect_redis, RedisDriver
from maidchan.config import ACCESS_TOKEN
from maidchan.helper import send_image
from pymessenger.bot import Bot

bot = Bot(ACCESS_TOKEN)


def main():
    # Connect to Redis
    rc = connect_redis(
        host='127.0.0.1',
        port=6379,
        db=0
    )
    redis_client = RedisDriver(rc)
    while True:
        # TODO: Update schedules metadata if it's empty or every 24 hours
        # TODO: Check all stored jobs
        time.sleep(60)

if __name__ == '__main__':
    main()
