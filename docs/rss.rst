=================
RSS Feed Notifier
=================

How It Works
------------

Maid-chan accepts RSS Feed subscription and sends out notification for each RSS update. By default, user can use 2 default preset:

- Manga via `mangaupdates.com`_

.. image:: https://freedomofkeima.com/images/maid-chan/rss_1_manga.png
    :alt: maidchan-rss-preset-manga
    :align: center
    :width: 300pt

- Nyaa (`nyaa.se`_)

.. image:: https://freedomofkeima.com/images/maid-chan/rss_1_nyaa.png
    :alt: maidchan-rss-preset-manga
    :align: center
    :width: 300pt

In addition, user can also use its own custom RSS Feed source.

.. image:: https://freedomofkeima.com/images/maid-chan/rss_2_custom.png
    :alt: maidchan-rss-preset-manga
    :align: center
    :width: 300pt

When the user subscribes using custom RSS, Maid-chan validates whether given URL has a valid RSS format via `feedparser`_ library.

.. autofunction:: maidchan.rss.is_valid_feed_url

Maid-chan uses regex comparison from user's input to the title of feed entries. Maid-chan stores list of all matched titles from the RSS Feed.

.. autofunction:: maidchan.rss.validate_and_create_entry

If there is a new title which is not stored in the database, Maid-chan will send out a notification to the user that a new update is available.

Initially, timestamp is used instead of list of titles. However, some sources (mangaupdates) don't provide timestamp information.

How to Run
----------

1. You can start running scheduler by executing:

.. code-block:: bash

   $ maidchan_scheduler

2. You can add & remove RSS to Maid-chan's RSS Feed notifier via `subscribe rss` and `unsubscribe rss` command in the Messenger.

.. _mangaupdates.com: https://www.mangaupdates.com/
.. _nyaa.se: https://www.nyaa.se/
.. _feedparser: https://github.com/kurtmckee/feedparser