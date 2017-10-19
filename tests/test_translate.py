# -*- coding: utf-8 -*-
import os

from mock import Mock, patch

from maidchan.translate import get_trans_language_prediction

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))


def _get_response(name):
    path = os.path.join(SCRIPT_PATH, 'data', name)
    with open(path) as f:
        return f.read()


class TestTranslate:
    @patch('subprocess.Popen')
    def test_get_translate_language_prediction(self, mock_subproc_open):
        process_mock = Mock()
        attrs = {'communicate.return_value': (
            _get_response('get_trans_prediction.txt'), None
        )}
        process_mock.configure_mock(**attrs)
        print(process_mock.communicate())
        mock_subproc_open.return_value = process_mock
        assert get_trans_language_prediction("Hello, World!") == "en"

