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
    get_kanji returns a single record of the current_pos line position

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
                kanji = dict(list(zip(KANJI_FIELDS, line)))
                break
    return kanji


def get_vocabulary(current_pos=1):
    """
    get_vocabulary returns a single record of the current_pos line position

    current_pos: up to number of records
    """
    vocabulary = {}
    with open(VOCABULARY_FILENAME, 'rb') as fobj:
        reader = csv.reader(fobj, delimiter=',', encoding='utf-8')
        num_of_lines = 0
        for line in reader:
            num_of_lines += 1
            if num_of_lines == current_pos:
                vocabulary = dict(list(zip(VOCABULARY_FIELDS, line)))
                break
    return vocabulary


def get_random_kanji(level):
    kanji_pos = randint(1, KANJI_TOTAL_RECORDS[level])
    return get_kanji(level, kanji_pos)


def get_random_vocabulary():
    vocab_pos = randint(1, VOCABULARY_TOTAL_RECORDS)
    return get_vocabulary(vocab_pos)


def get_japanese_message(kanji, vocab):
    message = "Welcome to Maid-chan's Daily Japanese lesson!\n\n"
    message += "Today Kanji is {}\nOn: {}\nKun: {}\nMeaning: {}\n\n".format(
        kanji["kanji"],
        kanji["on"],
        kanji["kun"],
        kanji["meaning"]
    )
    message += "----------\n\n"
    message += "Today Vocabulary is {}\nKanji: {}\nMeaning: {}\n\n".format(
        vocab["vocabulary"],
        vocab["kanji"],
        vocab["meaning"]
    )
    message += "See you tomorrow in the same section! <3"
    return message
