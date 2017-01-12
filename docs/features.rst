=================
Features Overview
=================

Features List
-------------

Currently, Maid-chan has the following features:

- :ref:`Image Processing with Primitive`: For every uploaded images to Maid-chan, Maid-chan will convert it to a geometric primitive GIF via `Primitive`_.

.. image:: https://freedomofkeima.com/images/maid-chan/primitive_scr.jpg
    :alt: maid-primitive-messenger
    :align: center
    :width: 300pt

.. image:: https://freedomofkeima.com/images/maid-chan/primitive.gif
    :alt: maid-primitive-gif
    :align: center
    :width: 300pt

- :ref:`Chatbot with ChatterBot`: For every text messages outside the provided available commands, Maid-chan will send a text response via `ChatterBot`_ and `langdetect`_ (to detect the language validity).

.. image:: https://freedomofkeima.com/images/maid-chan/chatterbot.png
    :alt: maid-chatbot-messenger
    :align: center
    :width: 300pt

- :ref:`Daily Offerings`: If user decides to subscribe for offerings feature, Maid-chan will send a good morning and a good night message with one additional image from `offerings/stock` directory.

.. image:: https://freedomofkeima.com/images/maid-chan/daily_morning_offerings.png
    :alt: maidchan-offerings-morning
    :align: center
    :width: 300pt

.. image:: https://freedomofkeima.com/images/maid-chan/daily_night_offerings.png
    :alt: maidchan-offerings-night
    :align: center
    :width: 300pt

- :ref:`Daily Japanese Lesson`: If user decides to subscribe for Japanese lesson feature, Maid-chan will send a Kanji (N1-N4, by choice) and a Vocabulary for each day.

.. image:: https://freedomofkeima.com/images/maid-chan/daily_japanese.png
    :alt: maidchan-japanese-messenger
    :align: center
    :width: 300pt

Currently, Maid-chan only supports `Asia/Tokyo` timezone (**UTC +9**).


Available Commands
------------------

All commands receive 2 parameters: `redis_client` as `RedisDriver` object and `recipient_id` as user's identifier.

.. autofunction:: maidchan.command.process_help

**help** is used to get the list of all available commands from Maid-chan.

.. autofunction:: maidchan.command.process_subscribe_offerings

**subscribe offerings** is used to subscribe daily offerings.

.. autofunction:: maidchan.command.process_unsubscribe_offerings

**unsubscribe offerings** is used to unsubscribe daily offerings.

.. autofunction:: maidchan.command.process_update_offerings

**update offerings** is used to update information (wake up & sleeping time) for daily offerings.

.. autofunction:: maidchan.command.process_subscribe_japanese

**subscribe japanese** is used to subscribe daily Japanese lesson.

.. autofunction:: maidchan.command.process_unsubscribe_japanese

**unsubscribe japanese** is used to unsubscribe daily Japanese lesson.

.. autofunction:: maidchan.command.process_update_japanese

**update japanese** is used to update information (Kanji N1-N4 level) for daily Japanese lesson.

.. autofunction:: maidchan.command.process_update_name

**update name** is used to change user's nickname. By default, Maid-chan will use `onii-chan` to call users.

.. autofunction:: maidchan.command.process_show_profile

**show profile** is used to show user's nickname, subscription status, and preference.

.. _Primitive: https://github.com/fogleman/primitive
.. _ChatterBot: https://github.com/gunthercox/ChatterBot
.. _langdetect: https://github.com/Mimino666/langdetect
