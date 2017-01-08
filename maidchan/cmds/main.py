# -*- coding: utf-8 -*-
import logging
import json
import sys
import tornado.ioloop
import tornado.web

from maidchan.base import connect_redis, RedisDriver
from maidchan.chatbot import ChatBotDriver
from maidchan.command import process_command, process_active_question
from maidchan.config import ACCESS_TOKEN, VERIFY_TOKEN
from maidchan.helper import validate_reserved_keywords, validate_attachments,\
    split_message
from pymessenger.bot import Bot

# Global init
bot = Bot(ACCESS_TOKEN)


def check_user_id(redis_client, recipient_id):
    users = redis_client.get_users()
    if recipient_id not in users:
        users.append(recipient_id)
        redis_client.set_users(users)
        logging.info("{} has just talked for the first time!".format(
            recipient_id
        ))


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
                # Append recipient_id to Maid-chan users list
                check_user_id(
                    self.application.redis_client,
                    recipient_id
                )
                logging.info("Sender ID: {}".format(recipient_id))
                if 'text' in fb_message:
                    query = fb_message['text']
                    # Check active question, if it's not active, continue
                    q_id = self.application.redis_client.get_active_question(
                        recipient_id
                    )
                    if q_id != -1:
                        # Process answer to Maid-chan questions
                        response = process_active_question(
                            self.application.redis_client,
                            recipient_id,
                            q_id,
                            query
                        )
                    elif validate_reserved_keywords(query.lower()):
                        # Process user's command
                        response = process_command(
                            self.application.redis_client,
                            recipient_id,
                            query.lower()
                        )
                    else:
                        # Normal chatbot
                        response = self.application.chatbot.get_response(query)
                    response_part = split_message(response)
                    for part in response_part:
                        bot.send_text_message(recipient_id, part)
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

