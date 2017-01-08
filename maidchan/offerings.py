# -*- coding: utf-8 -*-
from maidchan.constant import Constants


def get_morning_offerings_text():
    return Constants.NORMAL_GOOD_MORNING[0]


def get_night_offerings_text():
    return Constants.NORMAL_GOOD_NIGHT[0]


def get_offerings_image():
    # Ensure morning and night are different
    return "example.png", "example.png"
