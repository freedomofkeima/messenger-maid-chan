# -*- coding: utf-8 -*-
import logging
import json
import sys
import tornado.ioloop
import tornado.web

from random import randint

from maidchan.base import connect_redis, RedisDriver
from maidchan.chatbot import ChatBotDriver
from maidchan.config import ACCESS_TOKEN, VERIFY_TOKEN
from maidchan.japanese import get_kanji, get_vocabulary,\
    KANJI_TOTAL_RECORDS, VOCABULARY_TOTAL_RECORDS
from pymessenger.bot import Bot

RESERVED_KEYWORDS = [
    "subscribe"
]

# Global init
bot = Bot(ACCESS_TOKEN)


def test_message():
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
    return message


def validate_attachments(attachments):
    for attachment in attachments:
        if attachment.get('type') != 'image':
            return False
        url = attachment.get('payload', {}).get('url')
        if '.png' not in url and '.jpg' not in url:
            return False
    return True


def validate_reserved_keywords(command):
    for keyword in RESERVED_KEYWORDS:
        if keyword in command:
            return keyword
    return None


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
                fb_message = msg.get('message', {})
                recipient_id = msg['sender']['id']
                if 'text' in fb_message:
                    query = fb_message.get['text']
                    keyword = validate_reserved_keywords(query)
                    logging.info("Sender ID: {}".format(recipient_id))
                    if keyword:
                        response = test_message()
                    else:
                        response = self.application.chatbot.get_response(query)
                    bot.send_text_message(recipient_id, response)
                elif 'attachments' in fb_message:
                    is_valid = validate_attachments(fb_message['attachments'])
                    if not is_valid:
                        # We are not handling non-image data right now
                        bot.send_text_message(recipient_id, "いいねえ!")
                        continue
                    for attachment in fb_message['attachments']:
                        self.application.redis_client.push_primitive_queue({
                            "url": attachment.get('payload', {}).get('url'),
                            "recipient_id": recipient_id
                        })
                    bot.send_text_message(recipient_id, "しばらくねえ <3")
        self.write("Success")


def main():
    # Logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # Tornado Handler
    application = tornado.web.Application([
        (r"/webhook", WebhookHandler),
    ])

    # Connect to Redis
    rc = connect_redis(
        host='127.0.0.1',
        port=6379,
        db=0
    )
    application.redis_client = RedisDriver(rc)

    # Initialize Chatbot
    application.chatbot = ChatBotDriver()

    # Start app
    application.listen(9999)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

