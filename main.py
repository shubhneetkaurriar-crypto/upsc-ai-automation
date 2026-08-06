import feedparser

url = "https://news.google.com/rss/search?q=UPSC+current+affairs&hl=en-IN&gl=IN&ceid=IN:en"

feed = feedparser.parse(url)

print("Latest UPSC News:")

for article in feed.entries[:5]:
    print(article.title)
    print(article.link)
    print("-" * 50)
