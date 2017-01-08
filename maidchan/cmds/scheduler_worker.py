# -*- coding: utf-8 -*-
import concurrent.futures
import logging
import sys
import time

from maidchan.base import connect_redis, RedisDriver
from maidchan.config import ACCESS_TOKEN
from maidchan.helper import send_image
from maidchan.japanese import get_random_kanji, get_random_vocabulary,\
    get_japanese_message
from maidchan.offerings import get_morning_offerings_text,\
    get_night_offerings_text, get_offerings_image
from pymessenger.bot import Bot

bot = Bot(ACCESS_TOKEN)


def process_user(redis_client, recipient_id, metadata, current_mt):
    user = redis_client.get_user(recipient_id)
    schedules = user["schedules"]
    for schedule_type, mt in schedules.iteritems():
        if schedule_type == "morning_offerings_mt" and mt < current_mt:
            continue
        elif schedule_type == "night_offerings_mt" and mt < current_mt:
            continue
        elif schedule_type == "japanese_lesson_mt" and mt < current_mt:
            level = user["kanji_level"].lower()
            message = get_japanese_message(
                metadata["kanji_{}".format(level)],
                metadata["vocabulary"]
            )
            bot.send_text_message(recipient_id, message)
            user["schedules"]["japanese_lesson_mt"] += 86400
            redis_client.set_user(recipient_id, user)
            logging.info("Japanese scheduler for {} - {} is executed!".format(
                recipient_id,
                user["nickname"]
            ))


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Connect to Redis
    rc = connect_redis(
        host='127.0.0.1',
        port=6379,
        db=0
    )
    redis_client = RedisDriver(rc)
    while True:
        current_mt = int(time.time())
        metadata = redis_client.get_schedules()
        if not metadata or metadata["next_mt"] < current_mt:
            metadata["morning_offering_text"] = get_morning_offerings_text()
            metadata["night_offering_text"] = get_night_offerings_text()
            morning_image, night_image = get_offerings_image()
            metadata["morning_offering_image"] = morning_image
            metadata["night_offering_image"] = night_image
            metadata["kanji_n1"] = get_random_kanji(1)
            metadata["kanji_n2"] = get_random_kanji(2)
            metadata["kanji_n3"] = get_random_kanji(3)
            metadata["kanji_n4"] = get_random_kanji(4)
            metadata["vocabulary"] = get_random_vocabulary()
            metadata["next_mt"] = current_mt + 86400  # every 1 day
            redis_client.set_schedules(metadata)
        # Check all users (good enough if the number of users are small)
        recipient_ids = redis_client.get_users()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) \
            as executor:
            future_to_msg = \
                {executor.submit(
                    process_user,
                    redis_client,
                    recipient_id,
                    metadata,
                    current_mt
                ): recipient_id for recipient_id in recipient_ids}
            for future in concurrent.futures.as_completed(future_to_msg):
                try:
                    future.result()
                except Exception:
                    logging.exception("Error in scheduler!")
        time.sleep(60)


if __name__ == '__main__':
    main()
