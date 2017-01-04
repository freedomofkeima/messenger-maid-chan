# -*- coding: utf-8 -*-
import logging
import subprocess


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
