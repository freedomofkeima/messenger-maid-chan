===============
Daily Offerings
===============

How It Works
------------

Maid-chan has a scheduler worker for handling various daily tasks. For example, Maid-chan will send out daily good morning and good night greetings upon subscription. This feature is known as "Daily Offerings".

Daily offerings contain of two parts: greeting and image. Greetings are taken from `maidchan/constant.py` while offerings are taken from `offerings/stock/` directory.

.. autofunction:: maidchan.offerings.get_morning_offerings_text

.. autofunction:: maidchan.offerings.get_night_offerings_text

Offerings text functionality has two types: normal and special with 2% of probability. For example, Maid-chan sends morning greeting more than half an hour later than usual because of overslept. Greeting text on any specific day is the same for everyone, as it is stored in scheduler's metadata.

.. autofunction:: maidchan.offerings.get_offerings_image

.. autofunction:: maidchan.offerings.remove_offerings_image

In addition to text-based greetings, Maid-chan offers image as an addition. For all images which are stored under `offerings/stock/`, Maid-chan will pick 2 random images on daily basis for morning and night offerings. Each day, used offerings are moved to `offerings/used/` directory. If there is no image under `offerings/stock/` directory, Maid-chan will simply skip sending out images as a part of daily offerings.

How to Run
----------

1. You can start running scheduler by executing:

.. code-block:: bash

   $ maidchan_scheduler

2. You can subscribe & unsubscribe to Maid-chan's daily offerings via `subscribe offerings` and `unsubscribe offerings` command in the Messenger. Upon subscription, you will be asked 2 questions: your usual waking up time and your usual sleeping time.
