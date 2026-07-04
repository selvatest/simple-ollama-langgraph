import logging
from typing import Literal

from .config import FEED_URL, MAX_ITEMS
from .feed_service import fetch_feed_items
from .llm import llm
from .state import AgentState

logger = logging.getLogger(__name__)


def fetch_feed_node(state: AgentState) -> AgentState:
    feed_url = state.get("feed_url", FEED_URL)
    max_items = state.get("max_items", MAX_ITEMS)

    logger.info("Fetching feed from %s", feed_url)
    items, error = fetch_feed_items(feed_url, max_items)

    return {
        "items": items,
        "error": error,
    }


def route_after_fetch(state: AgentState) -> Literal["summarize_articles", "no_items"]:
    return "summarize_articles" if state.get("items") else "no_items"


def summarize_articles_node(state: AgentState) -> AgentState:
    summaries = []

    for index, item in enumerate(state["items"], start=1):
        prompt = f"""
You are a cybersecurity news assistant.

Summarize the following RSS item in exactly 3 short bullet points.
Keep it concise, factual, and useful.
Do not invent facts beyond the given content.

Title: {item['title']}
Link: {item['link']}
Content: {item['summary']}
"""

        try:
            response = llm.invoke(prompt)
            text = response.content if hasattr(response, "content") else str(response)

            summaries.append(
                f"Article {index}: {item['title']}\n"
                f"Link: {item['link']}\n"
                f"{text.strip()}"
            )
        except Exception as exc:
            logger.exception("Summarization failed for: %s", item["title"])
            summaries.append(
                f"Article {index}: {item['title']}\n"
                f"Link: {item['link']}\n"
                f"- Summarization failed: {exc}"
            )

    return {"article_summaries": summaries}


def build_digest_node(state: AgentState) -> AgentState:
    article_summaries = state.get("article_summaries", [])

    if not article_summaries:
        return {"final_digest": "No summaries available."}

    combined = "\n\n".join(article_summaries)

    prompt = f"""
You are a cybersecurity news digest assistant.

Using the article summaries below, create:
1. A short overall digest paragraph.
2. A section called 'Top Headlines'.
3. A section called 'Why It Matters'.

Keep it concise and readable.

Article summaries:
{combined}
"""

    try:
        response = llm.invoke(prompt)
        digest = response.content if hasattr(response, "content") else str(response)
        return {"final_digest": digest.strip()}
    except Exception as exc:
        logger.exception("Digest generation failed")
        return {"final_digest": f"Digest generation failed: {exc}"}


def no_items_node(state: AgentState) -> AgentState:
    return {"final_digest": state.get("error", "No feed items found.")}