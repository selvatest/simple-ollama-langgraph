from typing import List, TypedDict


class NewsItem(TypedDict):
    title: str
    link: str
    summary: str


class AgentState(TypedDict, total=False):
    feed_url: str
    max_items: int
    items: List[NewsItem]
    article_summaries: List[str]
    final_digest: str
    error: str