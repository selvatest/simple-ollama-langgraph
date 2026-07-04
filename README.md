# LangGraph RSS News Agent

A simple LangGraph project that fetches cybersecurity news from an RSS feed and summarizes it using a local Ollama model.

## Features

- Fetches latest RSS entries
- Routes workflow with LangGraph
- Summarizes each article with Ollama
- Creates a final digest
- Clean multi-file Python structure for learning

## Project structure

```text
langgraph_rss_news_agent/
├── rss_news_agent/
│   ├── __init__.py
│   ├── config.py
│   ├── feed_service.py
│   ├── graph_builder.py
│   ├── llm.py
│   ├── main.py
│   ├── nodes.py
│   └── state.py
├── run.py
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
ollama serve
ollama pull llama3.1:8b
python run.py
```

## Environment variables

- `OLLAMA_BASE_URL` default: `http://localhost:11434`
- `OLLAMA_MODEL` default: `llama3.1:8b`
- `FEED_URL` default: `https://feeds.feedburner.com/TheHackersNews`
- `MAX_ITEMS` default: `5`