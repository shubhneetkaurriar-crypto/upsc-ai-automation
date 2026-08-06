import os
import feedparser
from datetime import datetime
from supabase import create_client


# -----------------------------
# SUPABASE
# -----------------------------

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------
# SOURCES
# -----------------------------

RSS_FEEDS = {

    "Google News":
    "https://news.google.com/rss/search?q=UPSC+India+government+economy+environment+science&hl=en-IN&gl=IN&ceid=IN:en",

    "PIB":
    "https://pib.gov.in/RssMain.aspx",

    "RBI":
    "https://www.rbi.org.in/rss/PressReleases.xml",

    "PRS":
    "https://prsindia.org/rss"
}



# -----------------------------
# FETCH ARTICLES
# -----------------------------

def fetch_news():

    articles = []


    for source, url in RSS_FEEDS.items():

        try:

            print("Fetching:", source)

            feed = feedparser.parse(url)


            for item in feed.entries[:10]:

                articles.append({

                    "title": item.get("title",""),

                    "link": item.get("link",""),

                    "summary":
                    item.get("summary",
                    item.get("description","")),

                    "source": source

                })


        except Exception as e:

            print(
                source,
                "failed:",
                e
            )


    return articles



# -----------------------------
# DUPLICATE CHECK
# -----------------------------

def exists(title):

    result = (
        supabase
        .table("upsc_notes")
        .select("id")
        .eq("title", title)
        .execute()
    )

    return len(result.data) > 0



# -----------------------------
# GS CLASSIFICATION
# -----------------------------

def classify_gs(title):

    t = title.lower()


    if any(x in t for x in [
        "court",
        "parliament",
        "bill",
        "constitution",
        "government",
        "scheme"
    ]):
        return "GS2"


    if any(x in t for x in [
        "rbi",
        "inflation",
        "economy",
        "gdp",
        "bank"
    ]):
        return "GS3"


    if any(x in t for x in [
        "environment",
        "climate",
        "forest",
        "wildlife"
    ]):
        return "GS3"


    if any(x in t for x in [
        "isro",
        "space",
        "technology",
        "science"
    ]):
        return "GS3"


    if any(x in t for x in [
        "culture",
        "history",
        "heritage"
    ]):
        return "GS1"


    return "GS2"



# -----------------------------
# IMPORTANCE
# -----------------------------

def importance(title):

    score = 3

    words = [
        "supreme court",
        "budget",
        "rbi",
        "policy",
        "scheme",
        "international"
    ]


    for w in words:

        if w in title.lower():

            score += 1


    return min(score,5)



# -----------------------------
# SAVE
# -----------------------------

def save(article):

    data = {

        "date":
        datetime.now().strftime("%Y-%m-%d"),

        "title":
        article["title"],

        "source":
        article["link"],

        "gs_paper":
        classify_gs(article["title"]),

        "importance":
        importance(article["title"]),

        "notes":
        article["summary"]

    }


    supabase
    .table("upsc_notes")
    .insert(data)
    .execute()



# -----------------------------
# MAIN
# -----------------------------

def main():

    print("Starting UPSC collector")

    articles = fetch_news()

    print(
        "Total articles:",
        len(articles)
    )


    for article in articles:


        if not article["title"]:
            continue


        if exists(article["title"]):

            print(
                "Duplicate:",
                article["title"]
            )

            continue


        print(
            "Saving:",
            article["title"]
        )

        save(article)



    print(
        "Completed successfully"
    )



if __name__ == "__main__":

    main()
