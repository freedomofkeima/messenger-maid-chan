# -*- coding: utf-8 -*-
from maidchan.config import ACCESS_TOKEN, USERS
from pymessenger.bot import Bot

bot = Bot(ACCESS_TOKEN)

def main():
    for user in USERS:
        # Try to send message to all users
        bot.send_text_message(user[1], "{} bbbbaakaaa!".format(user[0]))
        # Try to send external link with button
        elements = []
        element = {
            "title": "Tanteeee",
            "image_url": "https://img.youtube.com/vi/DnSe9fbkas0/0.jpg",
            "default_action": {
                "type": "web_url",
                "url": "https://www.youtube.com/watch?v=DnSe9fbkas0"
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": "https://www.youtube.com/watch?v=DnSe9fbkas0",
                    "title": "This is a button"
                }
            ]
        }
        elements.append(element) 
        print bot.send_generic_message(user[1], elements)


if __name__ == "__main__":
    main()

