from langgraph.graph import END, START, StateGraph

from .nodes import (
    build_digest_node,
    fetch_feed_node,
    no_items_node,
    route_after_fetch,
    summarize_articles_node,
)
from .state import AgentState


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("fetch_feed", fetch_feed_node)
    graph.add_node("summarize_articles", summarize_articles_node)
    graph.add_node("build_digest", build_digest_node)
    graph.add_node("no_items", no_items_node)

    graph.add_edge(START, "fetch_feed")

    graph.add_conditional_edges(
        "fetch_feed",
        route_after_fetch,
        {
            "summarize_articles": "summarize_articles",
            "no_items": "no_items",
        },
    )

    graph.add_edge("summarize_articles", "build_digest")
    graph.add_edge("build_digest", END)
    graph.add_edge("no_items", END)

    return graph.compile()