=======================
Chatbot with ChatterBot
=======================

How It Works
------------

`ChatterBot`_ is a machine-learning based conversational dialog engine which is able to generate
responses based on collections of known conversations.

.. image:: https://freedomofkeima.com/images/maid-chan/chatterbot.png
    :alt: maid-chatbot-messenger
    :align: center
    :width: 300pt

.. autoclass:: maidchan.chatbot.ChatBotDriver

Maid-chan is trained with the provided Indonesian corpus, English corpus, and an additional corpus
which is stored at `maidcorpus`_ of this project (some of them are Japanese words). Each time a user
enters a statement, Chatterbot stores the text and its response for the next learning process.

ChatterBot is language independent, which means that Maid-chan could support 3 different languages
quite easily.

.. automethod:: maidchan.chatbot.ChatBotDriver.get_response_from_chatbot

.. automethod:: maidchan.chatbot.ChatBotDriver.get_response

The initial idea was to check whether user's language is in the supported list. However, it seems
the accuracy of `langdetect`_ is quite low, so it only checks whether the input is a valid language
or not (e.g.: emoticon).

Storage Adapter
---------------

By default, ChatterBot uses `chatterbot.storage.SQLStorageAdapter` as its storage adapter (since version 0.8.X).
For backwards compatibility reasons, we are using MongoDB adapter (`chatterbot.storage.MongoDatabaseAdapter`) as ChatterBot storage.

See http://chatterbot.readthedocs.io/en/stable/storage/index.html for full references.

Maid-chan Corpus
----------------

Maid-chan corpus consists of 3 files:

- conversations.corpus.json

- greetings.corpus.json

- trivia.corpus.json

You could append any other training materials as long as the file has the format of `corpus.json`.

.. _ChatterBot: https://github.com/gunthercox/ChatterBot
.. _maidcorpus: https://github.com/freedomofkeima/messenger-maid-chan/tree/master/maidcorpus
.. _langdetect: https://github.com/Mimino666/langdetect
