# -*- coding: utf-8 -*-
import logging
import os
from random import randint

from maidchan.constant import Constants

NORMAL = "normal"
SPECIAL = "special"

STOCK_OFFERINGS_PATH = "offerings/stock"
USED_OFFERINGS_PATH = "offerings/used"


def get_special_probability():
    p = randint(1, 100)
    if p <= 5:  # 5% chance of special
        logging.info("Special offerings for today!")
        return True
    logging.info("Normal offerings for today!")
    return False


def get_morning_offerings_text():
    is_special = get_special_probability()
    if is_special:
        p = randint(1, len(Constants.SPECIAL_GOOD_MORNING))
        return Constants.SPECIAL_GOOD_MORNING[p-1], SPECIAL
    else:
        p = randint(1, len(Constants.NORMAL_GOOD_MORNING))
        return Constants.NORMAL_GOOD_MORNING[p-1], NORMAL


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


def remove_offerings_image(filename):
    path = os.path.join(
        STOCK_OFFERINGS_PATH,
        filename
    )
    # Move file to used
    if os.path.isfile(path):
        os.rename(
            path,
            os.path.join(
                USED_OFFERINGS_PATH,
                filename
            )
        )
