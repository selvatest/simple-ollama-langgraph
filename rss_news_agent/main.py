import logging

from .config import FEED_URL, MAX_ITEMS
from .graph_builder import build_graph


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def run() -> None:
    app = build_graph()

    result = app.invoke(
        {
            "feed_url": FEED_URL,
            "max_items": MAX_ITEMS,
            "items": [],
            "article_summaries": [],
            "final_digest": "",
            "error": "",
        }
    )

    print("\n" + "=" * 100)
    print("FINAL DIGEST")
    print("=" * 100)
    print(result["final_digest"])

    print("\n" + "=" * 100)
    print("ARTICLE SUMMARIES")
    print("=" * 100)
    for summary in result.get("article_summaries", []):
        print(summary)
        print("-" * 100)


if __name__ == "__main__":
    run()