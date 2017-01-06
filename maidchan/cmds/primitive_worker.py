# -*- coding: utf-8 -*-
import errno
import shutil
import tempfile
import threading
import time

from maidchan.base import connect_redis, RedisDriver
from maidchan.config import ACCESS_TOKEN
from maidchan.helper import send_image
from maidchan.primitive import process_image
from pymessenger.bot import Bot

bot = Bot(ACCESS_TOKEN)


class ThreadHandler(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        try:
            d = tempfile.mkdtemp()  # create directory
            image_path, image_type = process_image(d, self.data.get('url', ""))
            if image_path and image_type:
                send_image(
                    ACCESS_TOKEN,
                    self.data.get('recipient_id', ""),
                    image_path,
                    image_type
                )
            else:
                bot.send_text_message(
                    self.data.get('recipient_id', ""),
                    "なにそれ？意味わかない!"
                )
        finally:
            # cleanup temporary directory
            try:
                shutil.rmtree(d)  # delete directory
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise


def main():
    # Connect to Redis
    rc = connect_redis(
        host='127.0.0.1',
        port=6379,
        db=0
    )
    redis_client = RedisDriver(rc)
    while True:
        data = redis_client.pop_primitive_queue()
        if not data:
            time.sleep(10)
            continue
        thread = ThreadHandler(data)
        thread.start()


if __name__ == '__main__':
    main()

