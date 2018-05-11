# -*- coding: utf-8 -*-
import calendar
import datetime
import logging
import os
import shutil
import subprocess
import time

from maidchan.constant import Constants


# TODO: Refactor send_text_message and send_image
def send_text_message(access_token, recipient_id, text, passive=False):
    """
    Note: MESSAGE_TAG is introduced to circumvent 24+1h window limit
    """
    args = [
        'curl',
        '-F',
        'recipient={"id":"%s"}' % recipient_id,
        '-F',
        'message={"text": "%s"}' % text
    ]
    if passive:
        args.append('-F')
        args.append('messaging_type=MESSAGE_TAG')
        args.append('-F')
        # Waiting for NON_PROMOTIONAL_SUBSCRIPTION
        args.append('tag=ACCOUNT_UPDATE')
    else:
        args.append('-F')
        args.append('messaging_type=RESPONSE')
    args.append(
        'https://graph.facebook.com/v2.7/me/messages?access_token={}'.format(
            access_token
        )
    )
    # Execute
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    if err:
        logging.error(err)


def send_image(access_token, recipient_id, image_path,
               image_type, passive=False):
    """
    Since pymessenger has a bug in sending image,
    we will use this method for time being
    """
    args = [
        'curl',
        '-F',
        'recipient={"id":"%s"}' % recipient_id,
        '-F',
        'message={"attachment":{"type":"image", "payload":{}}}',
        '-F',
        'filedata=@{};type={}'.format(image_path, image_type)
    ]
    if passive:
        args.append('-F')
        args.append('messaging_type=MESSAGE_TAG')
        args.append('-F')
        # Waiting for NON_PROMOTIONAL_SUBSCRIPTION
        args.append('tag=ACCOUNT_UPDATE')
    else:
        args.append('-F')
        args.append('messaging_type=RESPONSE')
    args.append(
        'https://graph.facebook.com/v2.7/me/messages?access_token={}'.format(
            access_token
        )
    )
    # Execute
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    if err:
        logging.error(err)


def validate_attachments(attachments):
    for attachment in attachments:
        if attachment.get('type') != 'image':
            return False
        url = attachment.get('payload', {}).get('url')
        if '.png' not in url and '.jpg' not in url:
            return False
    return True


def validate_reserved_keywords(command):
    for keyword in Constants.RESERVED_KEYWORDS:
        if command.startswith(keyword[0]):
            return True
    return False


def validate_translation_keywords(command):
    for keyword in Constants.TRANSLATION_KEYWORD:
        if command.startswith(keyword):
            return True
    return False


def split_message(message):
    """
    Apparently, Facebook has a text limit of 640
    We currently assume there's no line longer than 640
    """
    if len(message) <= 640:
        return [message]

    messages = []
    # Split based on new line
    d = "\n"
    lines = [e+d for e in message.split(d)]
    current_line = ""
    for line in lines:
        if len(current_line) + len(line) <= 640:
            current_line += line
        else:
            messages.append(current_line)
            current_line = line
    if current_line:
        messages.append(current_line)
    return messages


def time_to_next_utc_mt(time_str):
    dt = datetime.datetime.strptime(time_str, "%H:%M")  # UTC+9
    dt_now = datetime.datetime.now()  # Local timezone
    dt = dt.replace(
        year=dt_now.year,
        month=dt_now.month,
        day=dt_now.day
    )  # UTC+9
    dt = dt - datetime.timedelta(seconds=3600 * 9)  # UTC
    current_epoch_time = time.time()
    dt_epoch_time = int(calendar.timegm(dt.timetuple()))
    while dt_epoch_time < current_epoch_time:  # Move to the next day
        dt_epoch_time += 86400
    return dt_epoch_time


def copy_recursive(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_recursive(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) \
                    or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
