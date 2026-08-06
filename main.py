import os
import feedparser
from datetime import datetime
from supabase import create_client


# -----------------------------
# SUPABASE CONNECTION
# -----------------------------

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials missing")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------
# FETCH NEWS
# -----------------------------

def fetch_news():

    url = (
        "https://news.google.com/rss/search?"
        "q=India+government+OR+Supreme+Court+OR+economy+OR+environment+OR+ISRO+OR+international+relations"
        "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    articles = []

    for item in feed.entries[:15]:

        articles.append({
            "title": item.title,
            "link": item.link,
            "summary": item.get("summary", "")
        })

    return articles



# -----------------------------
# DUPLICATE CHECK
# -----------------------------

def already_exists(title):

    result = (
        supabase
        .table("upsc_notes")
        .select("title")
        .eq("title", title)
        .execute()
    )

    return len(result.data) > 0



# -----------------------------
# GS CLASSIFICATION
# -----------------------------

def classify_gs(title):

    text = title.lower()

    if any(word in text for word in [
        "supreme court",
        "parliament",
        "constitution",
        "bill",
        "election",
        "government",
        "policy"
    ]):
        return "GS2"

    if any(word in text for word in [
        "gdp",
        "economy",
        "rbi",
        "inflation",
        "budget",
        "tax"
    ]):
        return "GS3 Economy"

    if any(word in text for word in [
        "climate",
        "environment",
        "forest",
        "wildlife",
        "pollution"
    ]):
        return "GS3 Environment"

    if any(word in text for word in [
        "isro",
        "space",
        "ai",
        "technology",
        "science"
    ]):
        return "GS3 Science"

    if any(word in text for word in [
        "culture",
        "heritage",
        "history"
    ]):
        return "GS1"

    return "GS2"



# -----------------------------
# IMPORTANCE SCORE
# -----------------------------

def importance_score(title):

    important_words = [
        "supreme court",
        "bill",
        "policy",
        "rbi",
        "budget",
        "isro",
        "international"
    ]

    score = 3

    for word in important_words:
        if word in title.lower():
            score += 1

    return min(score, 5)



# -----------------------------
# SAVE TO SUPABASE
# -----------------------------

def save_article(article):

    record = {

        "date": datetime.now().strftime("%Y-%m-%d"),

        "title": article["title"],

        "source": article["link"],

        "gs_paper": classify_gs(
            article["title"]
        ),

        "importance": importance_score(
            article["title"]
        ),

        "notes": article["summary"]

    }

    supabase.table(
        "upsc_notes"
    ).insert(record).execute()



# -----------------------------
# MAIN
# -----------------------------

def main():

    print("Fetching news...")

    articles = fetch_news()

    print(
        "Found:",
        len(articles)
    )

    for article in articles:

        if already_exists(article["title"]):

            print(
                "Skipping duplicate:",
                article["title"]
            )

            continue


        print(
            "Saving:",
            article["title"]
        )

        save_article(article)


    print("Automation completed")



if __name__ == "__main__":
    main()
