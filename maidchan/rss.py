# -*- coding: utf-8 -*-
import feedparser
import re

# NOTE: If there is no pubdate, create one based on the topmost result
# If the topmost result is gone from the next RSS feed,
# assume all shown entries are newer than that