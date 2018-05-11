# -*- coding: utf-8 -*-
import concurrent.futures
import logging
import re
import sys
import time
from random import randint

from maidchan.base import connect_redis, RedisDriver
from maidchan.command import DEFAULT_NICKNAME
from maidchan.config import ACCESS_TOKEN
from maidchan.helper import send_text_message, send_image
from maidchan.japanese import get_random_kanji, get_random_vocabulary,\
    get_japanese_message
from maidchan.offerings import get_morning_offerings_text,\
    get_night_offerings_text, get_offerings_image, remove_offerings_image,\
    SPECIAL
from maidchan.rss import get_feed
from maidchan.train_status import get_train_status

from maidchan.helper import time_to_next_utc_mt


def send_offerings(recipient_id, text_message, image_path):
    if 'png' in image_path:
        image_type = "image/png"
    elif 'jpg' or 'jpeg' in image_path:
        image_type = "image/jpeg"
    else:
        image_type = None
    # Send good morning / good night message
    send_text_message(
        ACCESS_TOKEN,
        recipient_id,
        text_message,
        passive=True
    )
    # Send image offerings if file exists and recognizable
    if image_path and image_type:
        send_image(
            ACCESS_TOKEN,
            recipient_id,
            image_path,
            image_type,
            passive=True
        )


def process_user_schedules(redis_client, recipient_id, metadata, current_mt):
    user = redis_client.get_user(recipient_id)
    schedules = user["schedules"]
    for schedule_type, mt in schedules.items():
        if schedule_type == "morning_offerings_mt" and mt < current_mt:
            send_offerings(
                recipient_id,
                metadata["morning_offering_text"].format(
                    user.get("nickname", DEFAULT_NICKNAME)
                ),
                metadata["morning_offering_image"]
            )
            next_mt = time_to_next_utc_mt(user["night_time"])
            next_mt += metadata.get("night_offering_mt_offset", 0)
            del user["schedules"]["morning_offerings_mt"]  # Remove current item
            user["schedules"]["night_offerings_mt"] = next_mt
            redis_client.set_user(recipient_id, user)
            logging.info("Morning offerings for {} - {} is sent!".format(
                recipient_id,
                user.get("nickname", DEFAULT_NICKNAME)
            ))
        elif schedule_type == "night_offerings_mt" and mt < current_mt:
            send_offerings(
                recipient_id,
                metadata["night_offering_text"].format(
                    user.get("nickname", DEFAULT_NICKNAME)
                ),
                metadata["night_offering_image"]
            )
            next_mt = time_to_next_utc_mt(user["morning_time"])
            next_mt += metadata.get("morning_offering_mt_offset", 0)
            del user["schedules"]["night_offerings_mt"]  # Remove current item
            user["schedules"]["morning_offerings_mt"] = next_mt
            redis_client.set_user(recipient_id, user)
            logging.info("Night offerings for {} - {} is sent!".format(
                recipient_id,
                user.get("nickname", DEFAULT_NICKNAME)
            ))
        elif schedule_type == "japanese_lesson_mt" and mt < current_mt:
            level = user["kanji_level"].lower()
            try:
                message = get_japanese_message(
                    metadata["kanji_{}".format(level)],
                    metadata["vocabulary"]
                )
                send_text_message(
                    ACCESS_TOKEN,
                    recipient_id,
                    message,
                    passive=True
                )
            except Exception:
                pass
            while user["schedules"]["japanese_lesson_mt"] < int(time.time()):
                user["schedules"]["japanese_lesson_mt"] += 86400
            redis_client.set_user(recipient_id, user)
            logging.info("Japanese scheduler for {} - {} is executed!".format(
                recipient_id,
                user.get("nickname", DEFAULT_NICKNAME)
            ))


def process_user_rss(redis_client, recipient_id):
    user = redis_client.get_user(recipient_id)
    for key, entry in user["rss"].iteritems():
        feed = get_feed(entry["url"]).get("entries", {})
        for record in feed:
            title = record.get("title", "")
            try:
                m = re.search(
                    entry["pattern"].encode("utf-8").lower(),
                   title.lower()
                )
            except:
                m = None
            if m and title not in user["rss"][key]["title_list"]:
                url = entry["url"]
                if "link" in record:
                    url = record["link"]
                message = "\"{}\" in {} is now available, {}!".format(
                    title,
                    url,
                    user.get("nickname", DEFAULT_NICKNAME)
                )
                send_text_message(
                    ACCESS_TOKEN,
                    recipient_id,
                    message,
                    passive=True
                )
                user["rss"][key]["title_list"].append(title)
                redis_client.set_user(recipient_id, user)


def process_train_status(redis_client):
    notifications = []
    # Get stored / previous train status from DB
    prev_train_status = redis_client.get_train_status()
    # Get current train status
    cur_train_status = get_train_status()
    # Store current train status
    redis_client.set_train_status(cur_train_status)
    # Add newly occurred
    for cur in cur_train_status:
        is_existed = False
        for prev in prev_train_status:
            if prev["line"] == cur["line"]:
                is_existed = True
        if not is_existed:
            notifications.append(cur)
    # Check
    for prev in prev_train_status:
        is_resolved = True
        for cur in cur_train_status:
            # Not sure if normal operations is still parsed here ...
            if cur["status"] == "Normal operations":
                continue
            if prev["line"] == cur["line"]:
                is_resolved = False
                # Send out notification if status is changed
                if prev["status"] != cur["status"]:
                    notifications.append(cur)
        # Send out notification if status is resolved
        if is_resolved:
            notifications.append({
                "line": prev["line"],
                "status": "Normal operations"
            })
    return notifications


def process_train_notification(redis_client, recipient_id,
                               train_notifications):
    user = redis_client.get_user(recipient_id)
    if user.get("train_status", "unsubscribed") == "unsubscribed":
        return
    for notification in train_notifications:
        message = "{} Status Update:\n\n".format(
            notification["line"].encode("utf-8")
        )
        message += "Status: {}".format(
            notification["status"].encode("utf-8")
        )
        if notification.get("reason"):
            message += "\nReason: {}".format(
                notification["reason"].encode("utf-8")
            )
        send_text_message(
            ACCESS_TOKEN,
            recipient_id,
            message,
            passive=True
        )


def process_user(redis_client, recipient_id, metadata, current_mt,
                 train_notifications):
    # Process schedule-based operation
    process_user_schedules(
        redis_client,
        recipient_id,
        metadata,
        current_mt
    )
    # Process RSS-based operation
    process_user_rss(
        redis_client,
        recipient_id
    )
    # Process train notification operation
    if train_notifications is not None:
        process_train_notification(
            redis_client,
            recipient_id,
            train_notifications
        )


def adjust_offerings_mt(redis_client, users, metadata,
                        morning_offset, night_offset):
    m_adj = morning_offset - metadata.get("morning_offering_mt_offset", 0)
    n_adj = night_offset - metadata.get("night_offering_mt_offset", 0)
    for recipient_id in users:
        user = redis_client.get_user(recipient_id)
        schedules = user["schedules"]
        if "morning_offerings_mt" in schedules:
            user["schedules"]["morning_offerings_mt"] += m_adj
        if "night_offerings_mt" in schedules:
            user["schedules"]["night_offerings_mt"] += n_adj
        redis_client.set_user(recipient_id, user)


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
        recipient_ids = redis_client.get_users()
        current_mt = int(time.time())
        logging.info("Current epoch time is {}".format(current_mt))
        metadata = redis_client.get_schedules()
        if not metadata or metadata["next_mt"] < current_mt:
            # Get offerings text for today
            morning_text, morning_type = get_morning_offerings_text()
            metadata["morning_offering_text"] = morning_text
            if morning_type == SPECIAL:
                morning_offset = randint(2700, 5400)
            else:
                morning_offset = randint(0, 1800)
            night_text, night_type = get_night_offerings_text()
            metadata["night_offering_text"] = night_text
            if night_type == SPECIAL:
                night_offset = randint(2700, 3600)
            else:
                night_offset = randint(0, 900)

            # Adjust all users' offerings mt
            adjust_offerings_mt(
                redis_client,
                recipient_ids,
                metadata,
                morning_offset,
                night_offset
            )

            metadata["morning_offering_mt_offset"] = morning_offset
            metadata["night_offering_mt_offset"] = night_offset

            # Move old images
            if metadata.get("morning_offering_image"):
                remove_offerings_image(metadata["morning_offering_image"])
            if metadata.get("night_offering_image"):
                remove_offerings_image(metadata["night_offering_image"])

            # Get offerings image for today
            morning_image, night_image = get_offerings_image()
            metadata["morning_offering_image"] = morning_image
            metadata["night_offering_image"] = night_image

            # Get daily Kanji & Vocabulary
            metadata["kanji_n1"] = get_random_kanji(1)
            metadata["kanji_n2"] = get_random_kanji(2)
            metadata["kanji_n3"] = get_random_kanji(3)
            metadata["kanji_n4"] = get_random_kanji(4)
            metadata["vocabulary"] = get_random_vocabulary()

            # Set next_mt
            if "next_mt" not in metadata:
                metadata["next_mt"] = current_mt
            metadata["next_mt"] += 86400  # every 1 day

            # Save to DB
            redis_client.set_schedules(metadata)
        # Get train status
        try:
            train_notifications = process_train_status(redis_client)
        except:
            train_notifications = None
        # Check all users (good enough if the number of users are small)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) \
            as executor:
            future_to_msg = \
                {executor.submit(
                    process_user,
                    redis_client,
                    recipient_id,
                    metadata,
                    current_mt,
                    train_notifications
                ): recipient_id for recipient_id in recipient_ids}
            for future in concurrent.futures.as_completed(future_to_msg):
                try:
                    future.result(timeout=30)
                except Exception:
                    logging.exception("Error in scheduler!")
        time.sleep(60)


if __name__ == '__main__':
    main()
