# -*- coding: utf-8 -*-
import unicodecsv as csv
from random import randint

KANJI_FILENAMES = {
    1: "data/japanese_kanji_N1.csv",
    2: "data/japanese_kanji_N2.csv",
    3: "data/japanese_kanji_N3.csv",
    4: "data/japanese_kanji_N4.csv"
}

# TODO: Calculate total records on initialization
KANJI_TOTAL_RECORDS = {
    1: 1150,
    2: 739,
    3: 165,
    4: 80
}

VOCABULARY_FILENAME = "data/japanese_vocabulary_N1-4.csv"
VOCABULARY_TOTAL_RECORDS = 7539

KANJI_FIELDS = [
    "kanji",
    "on",
    "kun",
    "meaning"
]

VOCABULARY_FIELDS = [
    "vocabulary",
    "kanji",
    "meaning"
]


def get_kanji(level, current_pos=1):
    """
    get_kanji return a single record of the current_pos line position

    level: 1 - 4 (N1 to N4)
    current_pos: up to number of records
    """
    kanji = {}
    with open(KANJI_FILENAMES[level], 'rb') as fobj:
        reader = csv.reader(fobj, delimiter=',', encoding='utf-8')
        num_of_lines = 0
        for line in reader:
            num_of_lines += 1
            if num_of_lines == current_pos:
                kanji = dict(zip(KANJI_FIELDS, line))
                break
    # Convert to UTF-8
    for key, value in kanji.iteritems():
        kanji[key] = value.encode("utf-8")
    return kanji


def get_vocabulary(current_pos=1):
    """
    get_vocabulary return a single record of the current_pos line position

    current_pos: up to number of records
    """
    vocabulary = {}
    with open(VOCABULARY_FILENAME, 'rb') as fobj:
        reader = csv.reader(fobj, delimiter=',', encoding='utf-8')
        num_of_lines = 0
        for line in reader:
            num_of_lines += 1
            if num_of_lines == current_pos:
                vocabulary = dict(zip(VOCABULARY_FIELDS, line))
                break
    # Convert to UTF-8
    for key, value in vocabulary.iteritems():
        vocabulary[key] = value.encode("utf-8")
    return vocabulary


# THIS IS A TEST FUNCTION
def test_japanese_message():
    # Try N3
    level = 3
    kanji_pos = randint(1, KANJI_TOTAL_RECORDS[level])
    kanji = get_kanji(level, kanji_pos)
    vocab_pos = randint(1, VOCABULARY_TOTAL_RECORDS)
    vocab = get_vocabulary(vocab_pos)

    m1 = "Kanji: {}\nOn: {}\nKun: {}\nMeaning: {}".format(
        kanji["kanji"],
        kanji["on"],
        kanji["kun"],
        kanji["meaning"]
    )

    m2 = "Vocabulary: {}\nKanji: {}\nMeaning: {}".format(
        vocab["vocabulary"],
        vocab["kanji"],
        vocab["meaning"]
    )

    message = m1 + "\n---\n\n" + m2
    return message
