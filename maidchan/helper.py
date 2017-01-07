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
