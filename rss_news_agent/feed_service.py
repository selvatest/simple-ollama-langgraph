import logging
from typing import List

import feedparser

from .state import NewsItem

logger = logging.getLogger(__name__)


def fetch_feed_items(feed_url: str, max_items: int) -> tuple[List[NewsItem], str]:
    feed = feedparser.parse(feed_url)

    if getattr(feed, "bozo", 0):
        logger.warning(
            "Feed parsing warning: %s",
            getattr(feed, "bozo_exception", "unknown error"),
        )

    entries = feed.entries[:max_items]
    if not entries:
        return [], "No feed entries found."

    items: List[NewsItem] = []
    for entry in entries:
        items.append(
            {
                "title": getattr(entry, "title", "Untitled"),
                "link": getattr(entry, "link", ""),
                "summary": entry.get(
                    "summary",
                    entry.get("description", "No summary available")
                ),
            }
        )

    return items, ""