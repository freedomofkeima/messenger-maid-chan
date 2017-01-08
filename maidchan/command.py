# -*- coding: utf-8 -*-
from random import randint

from maidchan.constant import Constants
from maidchan.japanese import get_kanji, get_vocabulary,\
    KANJI_TOTAL_RECORDS, VOCABULARY_TOTAL_RECORDS


def test_message():
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


def process_command(redis_client, recipient_id, query):
    # TODO: Check admin status (for admin-only help menu)
    if query == "subscribe offerings":
        return process_subscribe_offerings(redis_client, recipient_id)
    elif query == "unsubscribe offerings":
        return process_unsubscribe_offerings(redis_client, recipient_id)
    elif query == "update offerings":
        return process_update_offerings(redis_client, recipient_id)
    elif query == "subscribe japanese":
        return process_subscribe_japanese(redis_client, recipient_id)
    elif query == "unsubscribe japanese":
        return process_unsubscribe_japanese(redis_client, recipient_id)
    elif query == "update japanese":
        return process_update_japanese(redis_client, recipient_id)
    elif query == "update name":
        return process_update_name(redis_client, recipient_id)
    elif query == "show profile":
        return process_show_profile(redis_client, recipient_id)
    # query "help" as default query
    return process_help(redis_client, recipient_id)


def process_active_question(redis_client, recipient_id, question_id, query):
    redis_client.set_active_question(recipient_id, -1)  # Set back to default
    if question_id == 1:
        return process_morning_question(redis_client, recipient_id, query)
    elif question_id == 2:
        return process_night_question(redis_client, recipient_id, query)
    elif question_id == 3:
        return process_kanji_level_question(redis_client, recipient_id, query)
    elif question_id == 4:
        return process_update_name_question(redis_client, recipient_id, query)
    return "<3"


def process_help(redis_client, recipient_id):
    user = redis_client.get_user(recipient_id)
    message = "Hello {}, welcome to Maid-chan Help System!\n\n".format(
        user.get("nickname", "onii-chan")
    )
    message += "You could ask me for these commands:\n"
    for keyword in Constants.RESERVED_KEYWORDS:
        message += "- \"{}\": {}\n".format(
            keyword[0],
            keyword[1]
        )
    message += "And also, time is handled in UTC+9, te-hee~"
    return message


def process_subscribe_offerings(redis_client, recipient_id):
    return test_message()


def process_unsubscribe_offerings(redis_client, recipient_id):
    return test_message()


def process_update_offerings(redis_client, recipient_id):
    return test_message()


def process_subscribe_japanese(redis_client, recipient_id):
    return test_message()


def process_unsubscribe_japanese(redis_client, recipient_id):
    return test_message()


def process_update_japanese(redis_client, recipient_id):
    return test_message()


def process_update_name(redis_client, recipient_id):
    return test_message()


def process_show_profile(redis_client, recipient_id):
    user = redis_client.get_user(recipient_id)
    message = "Hi, {}!\n".format(user.get("nickname", "onii-chan"))
    if not user.get("nickname"):
        message += "Maid-chan haven't learned how to call you properly :'(\n\n"
    message += "Offerings status: {}\n".format(user["offerings_status"])
    if user["offerings_status"] == "subscribed":
        message += "Morning message: around {} UTC+9\n".format(
            user["morning_time"]
        )
        message += "Night message: around {} UTC+9\n".format(
            user["night_time"]
        )
    message += "Japanese status: {}\n".format(user["japanese_status"])
    if user["japanese_status"] == "subscribed":
        message += "Kanji level: {}".format(user["kanji_level"])
    return message


def process_morning_question(redis_client, recipient_id, query):
    return test_message()


def process_night_question(redis_client, recipient_id, query):
    return test_message()


def process_kanji_level_question(redis_client, recipient_id, query):
    return test_message()


def process_update_name_question(redis_client, recipient_id, query):
    # Ensure name is not empty or space-only
    return test_message()
