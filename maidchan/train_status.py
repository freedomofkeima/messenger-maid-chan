# -*- coding: utf-8 -*-
#
# Code is partially adapted from https://github.com/ojii/tokyotrainstatus
# Copyright to Jonas Obrist (@ojii)
#
import requests
from bs4 import BeautifulSoup
from re import compile as c
from maidchan.translate import get_translation

STATUS_URL = "https://transit.yahoo.co.jp/traininfo/area/4/"

LINES = {
    u'東急田園都市線': 'Tokyu Den-en-toshi Line',
    u'南武線[川崎～立川]': 'Nambu Line [Kawasaki-Tachikawa]',
    u'東急大井町線': 'Tokyu Oimachi Line'
}

STATUSES = {
    u'列車遅延': 'Delays',
    u'運転見合わせ': 'Operations temporarily suspended',
    u'運転状況': 'Delays and cancellations',
    u'平常運転': 'Normal operations',
    u'運転再開': 'Preparing to resume operations',
    u'交通障害情報': 'Traffic trouble information'
}

l = lambda s: lambda name, **kw: s.format(name=_line(name.strip()), **kw)

REASONS = {
    c(r'^大雪災害の影響で'): 'due to heavy snow',
    c(r'台風(?P<number>\d+)号の影響で、'): 'due to typhoon #{number}',
    c(r'大雨の影響で、'): 'due to heavy rain',
    c(r'(?P<from>\w+)～(?P<to>\w+)駅間で踏切内点検を'): (
        'due to inspection between {from} and {to}'
    ),
    c(r'(?P<name>\w+線)内で踏切内点検を'): (
        l('due to inspection on the {name} line')
    ),
    c(r'\d{1,2}:\d{2}頃、(?P<station>\w+)駅で発生し'): (
        'due to problems near {station} station'
    ),
    c(r'\d{1,2}:\d{2}頃、(?P<from>\w+)～(?P<to>\w+)駅…$'): (
        'between {from} and {to} station'
    ),
    c(r'強風の影響で、'): 'due to strong winds',
    c(r'雪の影響で、',): 'due to snow',
    c(r'(?P<name>\w+線)内での雪の影響で'): l('due to snow on the {name} line'),
    c(r'(?P<name>\w+線)内で発生した人身事故'): l(
        'due to accident on the {name} line'
    ),
    c(r'(?P<station>\w+)駅で発生した人身事故'): (
        'due to accident at {station} station'
    ),
    c(r'倒木の影響で'): 'due to a tree falling on the tracks',
    c(r'(?P<station>\w+)駅で発生した倒木'): (
        'due to a tree falling on the tracks near {station} station'
    ),
    c(r'(?P<name>\w+線)内で発生した倒木'): (
        'due to a tree falling on the tracks of {name} line'
    ),
    c(r'(?P<station>\w+)駅で信号関係点検'): (
        'due to signal troubles at {station} station'
    ),
    c(r'(?P<name>\w+線)内で発生した架線支障'): (
        'due to overhead wire troubles on the {name} line'
    ),
    c(r'(?P<station>\w+)駅で発生した架線支障'): (
        'due to overhead wire troubles at {station} station'
    ),
    c(r'除雪作業の影響で'): 'due to snow removal',
    c(r'車両故障の影響で'): 'due to vehicle malfunction'
}


def _reason(ja):
    for key, value in REASONS.iteritems():
        match = key.match(ja)
        if match:
            if callable(value):
                return value(**match.groupdict())
            else:
                return value.format(**match.groupdict())
    return ja + "\nAutomatic translation: " + get_translation(ja)


def _status(ja):
    return STATUSES.get(ja, ja)


def _line(ja):
    try:
        return LINES[ja]
    except KeyError:
        return ja


def _is_line_supported(ja):
    try:
        _ = LINES[ja]
        return True
    except KeyError:
        return False


def parse_information(group_triples):
    result = []
    for triple in group_triples:
        line_tag, status_tag, info_tag = triple
        line = line_tag.a.text
        status = (
            status_tag.select('span.colTrouble')[0].text
            if status_tag.select('span.colTrouble')
            else status_tag.text
        ).strip()
        if _is_line_supported(line):
            result.append({
                'line': LINES[line],
                'status': _status(status),
                'reason': _reason(info_tag.text.strip())
            })
    return result


def get_train_status():
    r = requests.get(STATUS_URL)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.content, "html.parser")
    raw_data = soup.select('div.trouble table tr td')
    group_triples = [raw_data[x:x+3] for x in range(0, len(raw_data), 3)]
    information = parse_information(group_triples)
    return information
