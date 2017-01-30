=====================
Daily Japanese Lesson
=====================

How It Works
------------

One of the functionality of Maid-chan's scheduler worker is daily Japanese lesson. Currently, daily Japanese lesson sends a random kanji based on user's level selection (N1 - N4) and a random vocabulary (same for all levels) every 13:00 UTC+9.

.. image:: https://freedomofkeima.com/images/maid-chan/daily_japanese.png
    :alt: maidchan-japanese-messenger
    :align: center
    :width: 300pt

The raw data is parsed from `Gakuran`_ and currently stored under `data/` directory.

.. autofunction:: maidchan.japanese.get_kanji

Since the source data follows old format of JLPT test, there are only 4 levels in it: N1 to N4. `get_kanji` reads a certain line (`current_pos`) based on level selection from the file and returns it to the caller.

.. autofunction:: maidchan.japanese.get_vocabulary

The original data does not distinguish vocabulary based on JLPT levels. Therefore, it only accepts a certain line (`current_pos`), reads it from the file, and returns it to the caller.

.. autofunction:: maidchan.japanese.get_japanese_message

Finally, scheduler calls `get_japanese_message` to construct a daily lesson message.

How to Run
----------

1. You can start running scheduler by executing:

.. code-block:: bash

   $ maidchan_scheduler

2. You can subscribe & unsubscribe to Maid-chan's daily Japanese lesson via `subscribe japanese` and `unsubscribe japanese` command in the Messenger.

.. _Gakuran: http://gakuran.com/japanese-csv-database/
