# -*- coding: utf-8 -*-
import json
import tornado.ioloop
import tornado.web

from maidchan.config import ACCESS_TOKEN, VERIFY_TOKEN
from pymessenger.bot import Bot

bot = Bot(ACCESS_TOKEN)


class WebhookHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.request.arguments
        if args['hub.mode'][0] == 'subscribe' and \
           args['hub.verify_token'][0] == VERIFY_TOKEN:
            self.write(args['hub.challenge'][0])
            return
        self.set_status(403)

    def post(self):
        body = json.loads(self.request.body)
        print body
        for event in body['entry']:
            messaging = event['messaging']
            for msg in messaging:
                if msg.get('message'):
                    recipient_id = msg['sender']['id']
                    print "Sender ID: {}".format(recipient_id)
                    if msg['message'].get('text'):
                        message = msg['message']['text']
                        bot.send_text_message(recipient_id, message)
                    else:
                        pass
        self.write("Success")


def main():
    application = tornado.web.Application([
        (r"/webhook", WebhookHandler),
    ])
    application.listen(9999)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

