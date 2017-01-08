# -*- coding: utf-8 -*-
import logging
import subprocess

from maidchan.constant import Constants


def send_image(access_token, recipient_id, image_path, image_type):
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
        'filedata=@{};type={}'.format(image_path, image_type),
        'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(
            access_token
        )
    ]
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
        if keyword[0] in command:
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
            current_line = ""
    if current_line:
        messages.append(current_line)
    return messages
