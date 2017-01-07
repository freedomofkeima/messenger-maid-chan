# -*- coding: utf-8 -*-


class Constants(object):
    RESERVED_KEYWORDS = [
        ("help", "Maid-chan will show you these texts"),
        ("subscribe offerings", "Maid-chan will start sending a good morning & a good night messages"),
        ("unsubscribe offerings", "Maid-chan will stop sending you a good morning & a good night messages, but Maid-chan will be sad :'("),
        ("update offerings", "Maid-chan will keep her best to follow your waking up and sleeping time pattern!"),
        ("subscribe japanese", "Maid-chan will start sending you daily Japanese Kanji & Vocabulary"),
        ("unsubscribe japanese", "Maid-chan will stop sending you daily Japanese Kanji & Vocabulary"),
        ("update name", "What name do you prefer to be called? onii-chan? goshujin-sama? or ... darling?")
    ]

    QUESTIONS = {
        "1": "What time do you usually wake up in the morning, {}? (e.g.: 9:00)",
        "2": "What time do you usually sleep, {}? (e.g.: 23:00)",
        "3": "Which level of Kanji do you want to learn between N1-N4, {}? (e.g.: N3)"
    }

    NORMAL_GOOD_MORNING = [
        "おはよう! Wishing you a good day ahead, {} <3",
        "Ohaa~ I had a nice dream last night. Hope {} also had one!",
        "Good morning, {}. I feel you will have a nice day today!"
    ]

    NORMAL_GOOD_NIGHT = [
        "おやすみ, {}! Have a nice dream and rest tonight <3",
        "Oyasumi~ Today was fun and thanks for keep talking with me, nyaa~",
        "Good night, {}. I hope you will have a nice sleep tonight zzz..."
    ]

    SPECIAL_GOOD_MORNING = [
        "Kyaaaah! Maid-chan overslept today, やばい やばい! Good morning, {}~"
    ]

    SPECIAL_GOOD_NIGHT = [
        "Ah no, it's already this late! Good night, {} <3"
    ]
