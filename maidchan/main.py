# -*- coding: utf-8 -*-
import logging
import json
import redis
import sys
import time
import tornado.ioloop
import tornado.web

from random import randint

from maidchan.config import ACCESS_TOKEN, VERIFY_TOKEN
from maidchan.japanese import get_kanji, get_vocabulary,\
    KANJI_TOTAL_RECORDS, VOCABULARY_TOTAL_RECORDS
from pymessenger.bot import Bot

bot = Bot(ACCESS_TOKEN)


class WebhookHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        if args.get('hub.mode', [''])[0] == 'subscribe' and \
           args.get('hub.verify_token', [''])[0] == VERIFY_TOKEN:
            logging.info("Challenge endpoint is called")
            self.write(args['hub.challenge'][0])
            return
        self.set_status(403)

    def post(self):
        body = json.loads(self.request.body)
        logging.info(body)
        for event in body.get('entry', []):
            messaging = event['messaging']
            for msg in messaging:
                if msg.get('message'):
                    recipient_id = msg['sender']['id']
                    logging.info("Sender ID: {}".format(recipient_id))

                    # Try N3
                    level = 3
                    kanji_pos = randint(1, KANJI_TOTAL_RECORDS[level])
                    kanji = get_kanji(level, kanji_pos)
                    vocab_pos = randint(1, VOCABULARY_TOTAL_RECORDS)
                    vocab = get_vocabulary(vocab_pos)

                    m1 = "Kanji: {}\nOn: {}\nKun: {}\nMeaning: {}".format(
                        kanji["kanji"],
                        kanji["on"],
                        kanji["kun"],
                        kanji["meaning"]
                    )

                    m2 = "Vocabulary: {}\nKanji: {}\nMeaning: {}".format(
                        vocab["vocabulary"],
                        vocab["kanji"],
                        vocab["meaning"]
                    )

                    message = m1 + "\n---\n\n" + m2

                    bot.send_text_message(recipient_id, message)
                    #if msg['message'].get('text'):
                    #    message = msg['message']['text']
                    #    bot.send_text_message(recipient_id, message)
                    #else:
                    #    pass
        self.write("Success")


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Tornado Handler
    application = tornado.web.Application([
        (r"/webhook", WebhookHandler),
    ])

    # Connect to Redis
    val = None
    while val is None:
        try:
            r = redis.StrictRedis(host='127.0.0.1',
                                  port=6379,
                                  db=0)
            val = r.dbsize()
            application.redis_client = r
        except Exception:
            logging.exception("Cannot connect to Redis - Wait 30 seconds")
            time.sleep(30)

    # Start app
    application.listen(9999)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

