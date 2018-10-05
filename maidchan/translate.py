# -*- coding: utf-8 -*-
import logging
import shlex
import subprocess
from threading import Timer
from maidchan.constant import Constants


def get_trans_language_prediction(text):
    args = [
        "trans",
        "-id",
        text
    ]
    # Execute
    output = b""
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    timer = Timer(10, p.kill)  # Wait for 10 seconds
    try:
        timer.start()
        (output, err) = p.communicate()
        if err:
            logging.error(err)
    finally:
        timer.cancel()
    for key, val in list(Constants.TRANSLATION_DETECT.items()):
        if key in output.decode("utf-8"):
            return val
    return ""


def get_translation(query):
    # Initialize
    source_language_str = None
    target_language_str = None

    # Split
    try:
        elements = shlex.split(query)
    except Exception:
        elements = [query]
    source_list = []
    skip = False
    for index, element in enumerate(elements):
        if element in Constants.TRANSLATION_KEYWORD or skip:
            skip = False
            continue
        elif element in Constants.TRANSLATION_FROM:
            if index < len(elements) - 1:
                source_language_str = elements[index + 1]
                skip = True
        elif element in Constants.TRANSLATION_TO:
            if index < len(elements) - 1:
                target_language_str = elements[index + 1]
                skip = True
        else:
            source_list.append(element)
    source_text = " ".join(source_list)

    # Find language mapping
    source_language_key = None
    target_language_key = None
    for key, val in list(Constants.TRANSLATION_LANGUAGE.items()):
        if source_language_str in val:
            source_language_key = key
        if target_language_str in val:
            target_language_key = key

    # Use trans online language detection
    if not source_language_key:
        source_language_key = get_trans_language_prediction(source_text)
    # Use default mapping
    if not target_language_key:
        target_language_key = Constants.TRANSLATION_MAP[source_language_key]

    args = [
        "trans",
        "-b",
        "{}:{}".format(source_language_key, target_language_key),
        source_text
    ]

    # Execute
    output = b""
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    timer = Timer(10, p.kill)  # Wait for 10 seconds
    try:
        timer.start()
        (output, err) = p.communicate()
        if err:
            logging.error(err)
    finally:
        timer.cancel()

    return output.decode("utf-8")
