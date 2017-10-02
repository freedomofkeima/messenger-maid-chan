# -*- coding: utf-8 -*-
import datetime
import logging
import os
import pytz
from random import randint

from maidchan.constant import Constants

NORMAL = "normal"
SPECIAL = "special"

STOCK_OFFERINGS_PATH = "offerings/stock"
USED_OFFERINGS_PATH = "offerings/used"


def get_special_probability():
    p = randint(1, 100)
    if p <= 2:  # 2% chance of special
        logging.info("Special offerings for today!")
        return True
    logging.info("Normal offerings for today!")
    return False


def check_event_morning_offerings():
    result = []
    dt_now = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))  # UTC+9
    for event in Constants.EVENT_GOOD_MORNING:
        start_mt = dt_now.replace(
            month=event["start_month"],
            day=event["start_date"],
            hour=0,
            minute=0,
            second=0
        )
        end_mt = dt_now.replace(
            month=event["end_month"],
            day=event["end_date"],
            hour=23,
            minute=59,
            second=59
        )
        # Ensure start < end
        if end_mt < start_mt:
            end_mt = end_mt.replace(year=end_mt.year + 1)
        # Check range
        if start_mt <= dt_now <= end_mt:
            if event.get('force', False):
                return True, event["text"]
            else:
                result.append(event["text"])
    return False, result


def get_morning_offerings_text():
    # Priority: event force > special > normal/event
    event_force, event_text = check_event_morning_offerings()
    # Force special text, e.g.: Halloween day, Christmas day, etc
    if event_force:
        return event_text, NORMAL
    is_special = get_special_probability()
    if is_special:
        p = randint(1, len(Constants.SPECIAL_GOOD_MORNING))
        return Constants.SPECIAL_GOOD_MORNING[p-1], SPECIAL
    else:
        text_list = Constants.NORMAL_GOOD_MORNING + event_text
        p = randint(1, len(text_list))
        return text_list[p-1], NORMAL


def get_night_offerings_text():
    is_special = get_special_probability()
    if is_special:
        p = randint(1, len(Constants.SPECIAL_GOOD_NIGHT))
        return Constants.SPECIAL_GOOD_NIGHT[p-1], SPECIAL
    else:
        p = randint(1, len(Constants.NORMAL_GOOD_NIGHT))
        return Constants.NORMAL_GOOD_NIGHT[p-1], NORMAL


def get_offerings_image():
    # Ensure morning and night are different
    stock_files = os.listdir(STOCK_OFFERINGS_PATH)
    if len(stock_files) < 2:
        return None, None
    p = randint(1, len(stock_files))
    p2 = p
    while p == p2:
        p2 = randint(1, len(stock_files))
    morning_image = os.path.join(STOCK_OFFERINGS_PATH, stock_files[p-1])
    night_image = os.path.join(STOCK_OFFERINGS_PATH, stock_files[p2-1])
    return morning_image, night_image


def remove_offerings_image(filepath):
    # Move file to used
    if os.path.isfile(filepath):
        os.rename(
            filepath,
            os.path.join(
                USED_OFFERINGS_PATH,
                os.path.basename(filepath)
            )
        )
