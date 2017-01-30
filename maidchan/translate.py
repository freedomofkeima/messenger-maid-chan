# -*- coding: utf-8 -*-
import logging
import shlex
import subprocess
from maidchan.constant import Constants


def get_trans_language_prediction(text):
    args = [
        "trans",
        "-id",
        text
    ]
    # Execute
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    if err:
        logging.error(err)
    for key, val in Constants.TRANSLATION_DETECT.iteritems():
        if key in output:
            return val
    return ""


def get_translation(query):
    # Initialize
    source_language_str = None
    target_language_str = None

    # Split
    elements = shlex.split(query.encode('utf-8'))
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
    for key, val in Constants.TRANSLATION_LANGUAGE.iteritems():
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
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    if err:
        logging.error(err)
        return ""

    return output
