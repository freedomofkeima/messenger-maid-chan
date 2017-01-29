# -*- coding: utf-8 -*-
import feedparser
import re
import time
from datetime import datetime


def is_valid_feed_url(url):
    try:
        response = feedparser.parse(url)
        if 'bozo_exception' in response:
            return False
    except Exception:
        return False
    return True


def validate_and_create_entry(url, pattern):
    if not url:
        return {}

    try:
        d = feedparser.parse(url)
    except Exception:
        return {}

    # Check whether entry currently exists
    ret = {
        "url": url,
        "pattern": pattern,
        "last_title": ""
    }
    is_pubdate_exist = False
    current_epoch = int(time.time())
    for entry in d.get("entries", {}):
        m = re.search(
            pattern.lower(),
            entry.get("title", "").lower()
        )
        if "published_parsed" in entry:
            is_pubdate_exist = True
        if m:
            if is_pubdate_exist:
                dt = datetime.fromtimestamp(
                    time.mktime(entry["published_parsed"])
                )
                feed_mt = int((dt - datetime(1970, 1, 1)).total_seconds())
                # Trigger first notification
                ret["timestamp"] = feed_mt - 1
            else:
                # Trigger first notification
                ret["timestamp"] = current_epoch - 1
            break

    if "timestamp" not in ret:
        ret["timestamp"] = current_epoch

    return ret
