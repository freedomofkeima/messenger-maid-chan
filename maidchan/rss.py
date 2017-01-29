# -*- coding: utf-8 -*-
import feedparser
import re


def is_valid_feed_url(url):
    try:
        response = feedparser.parse(url)
        if 'bozo_exception' in response:
            return False
    except Exception:
        return False
    return True


def get_feed(url):
    try:
        return feedparser.parse(url)
    except Exception:
        return {}


def validate_and_create_entry(url, pattern):
    if not url:
        return {}

    d = get_feed(url)
    if not d:
        return {}

    # Check whether entry currently exists
    ret = {
        "url": url,
        "pattern": pattern,
        "title_list": []
    }
    for entry in d.get("entries", {}):
        try:
            m = re.search(
                pattern.encode("utf-8").lower(),
                entry.get("title", "").lower()
            )
        except:
            m = None
        if m:
            ret["title_list"].append(entry.get("title", ""))

    return ret
