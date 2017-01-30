===================================
Translate text via Google Translate
===================================

How It Works
------------

Maid-chan feat `translate-shell`_ provide an interface to use Google Translate as translation tool via Facebook Messenger.

.. image:: https://freedomofkeima.com/images/maid-chan/translate_normal.png
    :alt: maidchan-translate-text
    :align: center
    :width: 300pt

.. image:: https://freedomofkeima.com/images/maid-chan/translate_using_from.png
    :alt: maidchan-translate-text
    :align: center
    :width: 300pt

.. autofunction:: maidchan.translate.get_translation

Initially, Maid-chan will identify the given message in 4 parts:

- "translate" keyword (or "terjemahkan" in Bahasa)
- "from" keyword outside quotes, which is used to identify source language
- "to" keyword outside quotes, which is used to identify target language
- source text for translation

Since there are multiple mapping possibilities ("id", "Indo", "Indonesia" have the same meaning),
"from" and "to" keywords are mapped to its appropriate language code.
Currently, Maid-chan supports Bahasa Indonesia, English, and Japanese.

.. autofunction:: maidchan.translate.get_trans_language_prediction

If Maid-chan could not recognize proper mapping, `get_trans_language_prediction` is called.
This function will use Google language detection to see whether Maid-chan could map source text into 1 out of 3 supported languages.

Several default rules in Maid-chan are:

- English will be translated to Japanese
- Japanese will be translated to English
- Bahasa Indonesia will be translated to Japanese
- Default source language is Google language detection and default target language is English


.. _translate-shell: https://github.com/soimort/translate-shell
