# -*- coding: utf-8 -*-
import os

from mock import Mock, patch

from maidchan.translate import get_trans_language_prediction, get_translation

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


def _get_response(name):
    path = os.path.join(SCRIPT_PATH, 'data', name)
    with open(path) as f:
        return f.read().encode("utf-8")


def mocked_trans(*args, **kwargs):
    """
    Mocked "trans"
    """
    process_mock = Mock()
    return_value = None
    if '-id' in args[0] and 'hello, world!' in args[0]:
        return_value = _get_response('get_trans_prediction.txt')
    elif '-b' in args[0] and 'en:ja' in args[0] and 'hello, world!' in args[0]:
        return_value = _get_response('get_trans_translation.txt')
    elif '-b' in args[0] and 'en:id' in args[0] and 'hello, world!' in args[0]:
        return_value = _get_response('get_trans_translation_2.txt')
    attrs = {'communicate.return_value': (return_value, None)}
    process_mock.configure_mock(**attrs)
    return process_mock


class TestTranslate:
    @patch('subprocess.Popen', side_effect=mocked_trans)
    def test_get_translate_language_prediction(self, mock_trans):
        assert get_trans_language_prediction("hello, world!") == "en"

    @patch('subprocess.Popen', side_effect=mocked_trans)
    def test_get_translation_en_to_ja(self, mock_trans):
        query = "translate hello, world! from english to japanese"
        assert get_translation(query) == "こんにちは世界！"

    @patch('subprocess.Popen', side_effect=mocked_trans)
    def test_get_translation_en_to_default(self, mock_trans):
        query = "translate hello, world! from english"
        assert get_translation(query) == "こんにちは世界！"

    @patch('subprocess.Popen', side_effect=mocked_trans)
    def test_get_translation_default_to_id(self, mock_trans):
        query = "translate hello, world! to bahasa"
        assert get_translation(query) == "Halo Dunia!"
