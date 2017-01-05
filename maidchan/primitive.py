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
    elif '.jpg' in url:
        filename = "input.jpg"

    if image_path and filename:
        # Download image to the specified directory
        urllib.urlretrieve(url, os.path.join(image_path, filename))
        return create_primitive_image(image_path, filename)
    return None, None


def create_primitive_image(image_path, filename):
    """
    create_primitive_image utilizes fogleman/primitive
    """
    for i in xrange(0, 3):  # Generate 3 different images
       output_path = os.path.join(image_path, "output{}.png".format(i))
       args = [
           'primitive',
           '-i',
            os.path.join(image_path, filename),
            '-o',
            output_path,
            '-n',
            '150',
            '-v'
        ]
        # Execute
        p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        if err:
            logging.error(err)
    return generate_gif_file_from_primitive(image_path, filename)


def generate_gif_file_from_primitive(image_path, filename):
    # Remove input file
    os.remove(os.path.join(image_path, filename))
    # Generate gif output
    output_path = os.path.join(image_path, "output.gif")
    args = [
        'convert',
        '-delay',
        '1x5',  # 5 FPS
        '-loop',
        '0',
        os.path.join(image_path, '*.png'),
        output_path
    ]
    # Execute
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    if err:
        logging.error(err)
    return output_path, "image/gif"
