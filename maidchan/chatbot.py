# -*- coding: utf-8 -*-
import logging
import os
import chatterbot.corpus
from chatterbot import ChatBot
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from maidchan.helper import copy_recursive


class ChatBotDriver(object):
    def __init__(self, storage_adapter):
        self.initialize()  # Initialize corpus files
        self.chatbot = ChatBot(
            'Maid-chan',
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
            output_adapter="chatterbot.output.OutputFormatAdapter",
            output_format='text',
            storage_adapter=storage_adapter
        )
        self.chatbot.train(
            "chatterbot.corpus.indonesia.conversations",
            "chatterbot.corpus.indonesia.greetings",
            "chatterbot.corpus.english.conversations",
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.maidcorpus"  # Custom!
        )
        logging.info("Chatterbot is initialized!")

    def initialize(self):
        """
        WARNING: Not exactly a correct way to do it
        """
        # Get installed path
        path = os.path.dirname(chatterbot.corpus.__file__)
        # Put maidcorpus to the destination path
        data_path = os.path.join(path, "data", "maidcorpus")
        copy_recursive("maidcorpus", data_path)

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
