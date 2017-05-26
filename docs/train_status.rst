===================================
Tokyo Train Status feat Yahoo Japan
===================================

How It Works
------------

Maid-chan feat `Yahoo`_ Japan provides real-time notification for Tokyo train status which are defined to be monitored.
Currently, there are 3 monitored train lines: Tokyu Den-en-toshi Line, Nambu Line, and Tokyu Oimachi Line.

.. image:: https://freedomofkeima.com/images/maid-chan/train_status.png
    :alt: maidchan-train-status
    :align: center
    :width: 300pt

.. autofunction:: maidchan.train_status.parse_information

.. autofunction:: maidchan.train_status.get_train_status

Since the retrieved data is HTML-formatted, we need to parse the data that we want with BeautifulSoup.
In addition, the raw data from Yahoo Japan is all written in Japanese, therefore, we need to do some pre-processing to translate those data to English.
When the translation is not found in the defined constant, Maid-chan's Google Translate feature is used for providing automatic translation.

Notification will be sent when the train status is changed, e.g.: from "Normal Operations" to "Operations temporarily suspended", from "Operations temporarily suspended" to "Delays", etc.

How to Run
----------

1. Ensure you have `translate-shell`_ installed (for automatic translation, see :ref:`Translate text via Google Translate`).

2. You can start running scheduler by executing:

.. code-block:: bash

   $ maidchan_scheduler

3. You can subscribe & unsubscribe to Maid-chan's Tokyo train status notification via `subscribe train` and `unsubscribe train` command in the Messenger.

Special Thanks
--------------

Special thanks to Jonas Obrist (ojii) for providing `tokyotrainstatus`_ codebase.

.. _Yahoo: https://transit.yahoo.co.jp/traininfo/area/4/
.. _translate-shell: https://github.com/soimort/translate-shell
.. _tokyotrainstatus: https://github.com/ojii/tokyotrainstatus
