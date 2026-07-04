import feedparser

feed_url = "https://feeds.feedburner.com/TheHackersNews"
feed = feedparser.parse(feed_url)

for entry in feed.entries[:3]:
    print("TITLE:", entry.title)
    print("LINK:", entry.link)
    print("SUMMARY:", entry.get("summary", "No summary"))
    print("-" * 80)