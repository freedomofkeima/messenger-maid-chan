# -*- coding: utf-8 -*-
from maidchan.base import connect_redis, RedisObject


def main():
    # Connect to Redis
    rc = connect_redis(
        host='127.0.0.1',
        port=6379,
        db=0
    )
    redis_client = RedisObject(rc)


if __name__ == '__main__':
    main()

