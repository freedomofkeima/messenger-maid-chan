==========
How to Run
==========

In order to run Maid-chan properly, you need to be able to use `Facebook Messenger Bot`_.

Maid-chan Installation
----------------------

1. Clone the code from Github.

.. code-block:: bash

   $ git clone https://github.com/freedomofkeima/messenger-maid-chan.git

2. You need to fill Facebook token information in `maidchan/config.py` based on `maidchan/config.py.example`.

.. code-block:: python

   # Facebook token
   ACCESS_TOKEN = "FACEBOOK_PAGE_ACCESS_TOKEN"
   VERIFY_TOKEN = "WEBHOOK_VERIFY_TOKEN"  # Set this value by yourself

   # Optional (recipient_id)
   ADMIN = [
       "123...9"
   ]

   # Chatbot storage
   STORAGE_ADAPTER = "chatterbot.storage.JsonFileStorageAdapter"

**ACCESS_TOKEN** is received when you are creating an application on Facebook.

**VERIFY_TOKEN** should be your secret token between Facebook and your application.

**ADMIN** is `recipient_id` of application's admin. The only way to get this value is from communicating
directly with your application, since `recipient_id` is not the same with user's Facebook ID and it
differs between applications.

**STORAGE_ADAPTER** is used to store Chatterbot learning data. By default, it will create `database.db`
in JSON format, but the performance gets slower as the number of data gets bigger. See `Chatterbot Documentation`_
or :ref:`Storage Adapter` for better reference.

3. Maid-chan is using Redis as the database. Redis can be downloaded via https://redis.io/download.
It's preferable to run Redis as a background process in port 6379 (default port).

.. code-block:: bash

   $ screen -R redis # use screen
   $ ... # run Redis in background

4. It is recommended to use `virtualenv` for running Python code. After that, you need to install all dependencies
which are specified in `requirements.txt`.

.. code-block:: bash

   $ python3 -m venv venv # create virtualenv
   $ source venv/bin/activate # start virtualenv
   $ pip install -r requirements.txt # install Maid-chan dependencies

5. Finally, you can create Maid-chan executables by executing:

.. code-block:: bash

   $ python setup.py install
   $ maidchan # start Maid-chan main logic

Maid-chan Executables
---------------------

Maid-chan has 3 executables (recommended to use `screen`):

- **maidchan**: Maid-chan main logic which is used to communicate with Facebook. It also handles user's input processing, such as :ref:`Chatbot with ChatterBot` and :ref:`Translate text via Google Translate`.

- **maidchan_primitive**: CPU intensive task which processes image with Machine Learning and returns an abstract GIF (:ref:`Image Processing with Primitive`).

- **maidchan_scheduler**: Scheduler which is used to handle daily and repetitive tasks, such as :ref:`Daily Offerings`, :ref:`Daily Japanese Lesson`, :ref:`RSS Feed Notifier`, and :ref:`Tokyo Train Status feat Yahoo Japan`.

.. _Facebook Messenger Bot: https://developers.facebook.com/docs/messenger-platform/guides/quick-start
.. _Chatterbot Documentation: http://chatterbot.readthedocs.io/en/stable/storage/index.html
