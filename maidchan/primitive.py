# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import urllib


def process_image(image_path, url):
    """
    process_image receives facebook URL and add primitive filter to it
    """
    filename = None
    if '.png' in url:
        filename = "input.png"
        image_type = "image/png"
    elif '.jpg' in url:
        filename = "input.jpg"
        image_type = "image/jpg"

    if image_path and filename:
        # Download image to the specified directory
        urllib.urlretrieve(url, os.path.join(image_path, filename))
        return create_primitive_image(image_path, image_type, filename)
    return None, None


def create_primitive_image(image_path, image_type, filename):
    """
    create_primitive_image utilizes fogleman/primitive
    """
    output_path = os.path.join(image_path, "output.png")
    args = [
        'primitive',
        '-i',
        os.path.join(image_path, filename),
        '-o',
        output_path,
        '-n',
        '1',
        '-v'
    ]
    # Execute
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    if err:
        logging.error(err)
    return output_path, image_type
