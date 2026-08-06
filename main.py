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
    raise Exception("Supabase keys missing")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------
# RSS SOURCES
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
# FETCH NEWS
# -----------------------------

def fetch_news():

    articles = []

    for source, url in RSS_FEEDS.items():

        print("Fetching:", source)

        try:

            feed = feedparser.parse(url)

            for item in feed.entries[:10]:

                articles.append({

                    "title": item.get("title", ""),

                    "link": item.get("link", ""),

                    "summary": item.get(
                        "summary",
                        item.get("description", "")
                    ),

                    "source": source

                })

        except Exception as e:

            print(
                source,
                "error:",
                e
            )

    return articles



# -----------------------------
# DUPLICATE CHECK
# -----------------------------

def already_exists(title):

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

    text = title.lower()


    if any(word in text for word in [
        "constitution",
        "supreme court",
        "parliament",
        "bill",
        "scheme",
        "government"
    ]):
        return "GS2"


    if any(word in text for word in [
        "economy",
        "rbi",
        "inflation",
        "gdp",
        "bank"
    ]):
        return "GS3 Economy"


    if any(word in text for word in [
        "environment",
        "climate",
        "forest",
        "wildlife"
    ]):
        return "GS3 Environment"


    if any(word in text for word in [
        "isro",
        "space",
        "technology",
        "science"
    ]):
        return "GS3 Science"


    if any(word in text for word in [
        "history",
        "culture",
        "heritage"
    ]):
        return "GS1"


    return "GS2"



# -----------------------------
# IMPORTANCE
# -----------------------------

def importance(title):

    score = 3

    keywords = [
        "supreme court",
        "budget",
        "rbi",
        "policy",
        "scheme",
        "international"
    ]


    for word in keywords:

        if word in title.lower():

            score += 1


    return min(score, 5)



# -----------------------------
# SAVE TO SUPABASE
# -----------------------------

def save_article(article):

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


    supabase.table(
        "upsc_notes"
    ).insert(data).execute()



# -----------------------------
# MAIN
# -----------------------------

def main():

    print("Starting UPSC News Automation")

    articles = fetch_news()

    print(
        "Articles found:",
        len(articles)
    )


    for article in articles:

        if not article["title"]:
            continue


        if already_exists(article["title"]):

            print(
                "Duplicate:",
                article["title"]
            )

            continue


        print(
            "Saving:",
            article["title"]
        )

        save_article(article)



    print(
        "Automation completed"
    )



if __name__ == "__main__":

    main()
