import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
FEED_URL = os.getenv("FEED_URL", "https://feeds.feedburner.com/TheHackersNews")
MAX_ITEMS = int(os.getenv("MAX_ITEMS", "5"))