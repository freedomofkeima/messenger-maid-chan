# -*- coding: utf-8 -*-
import logging
from chatterbot import ChatBot
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


class ChatBotDriver(object):
    def __init__(self):
        self.chatbot = ChatBot(
            'Maid-chan',
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
            output_adapter="chatterbot.output.OutputFormatAdapter",
            output_format='text'
        )
        self.chatbot.train(
            "chatterbot.corpus.indonesia",
            "chatterbot.corpus.english"
        )
        logging.info("Chatterbot is initialized!")

    def get_response_from_chatbot(self, query, language):
        if not language:
            return "nyaa <3"
        else:
            return self.chatbot.get_response(query)

    def get_response(self, query):
        try:
            probable_language = detect(query)
        except LangDetectException:
            probable_language = ""
        logging.info("Probable language is {}".format(probable_language))
        return self.get_response_from_chatbot(query, probable_language)
