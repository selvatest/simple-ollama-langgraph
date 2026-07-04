from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


class AgentState(TypedDict):
    input_text: str
    needs_summary: bool
    summary: str


llm = ChatOllama(
    model="llama3.1:8b",
    base_url="http://localhost:11434"
)

def read_input_node(state: AgentState):
    text = state["input_text"].strip()
    return {"input_text": text}


def check_length_node(state: AgentState):
    text = state["input_text"]
    return {"needs_summary": len(text.split()) > 20}


def summarize_node(state: AgentState):
    prompt = f"""
Summarize the following text in 3 short bullet points.

Text:
{state["input_text"]}
"""
    response = llm.invoke(prompt)
    return {"summary": response.content}


def skip_node(state: AgentState):
    return {"summary": "Input too short. Skipping summarization."}


def route_after_check(state: AgentState):
    return "summarize" if state["needs_summary"] else "skip"


graph = StateGraph(AgentState)
graph.add_node("read_input", read_input_node)
graph.add_node("check_length", check_length_node)
graph.add_node("summarize", summarize_node)
graph.add_node("skip", skip_node)

graph.add_edge(START, "read_input")
graph.add_edge("read_input", "check_length")
graph.add_conditional_edges("check_length", route_after_check)
graph.add_edge("summarize", END)
graph.add_edge("skip", END)

app = graph.compile()

if __name__ == "__main__":
    text = input("Paste text:\n")
    result = app.invoke({
        "input_text": text,
        "needs_summary": False,
        "summary": ""
    })
    print("\nResult:\n")
    print(result["summary"])