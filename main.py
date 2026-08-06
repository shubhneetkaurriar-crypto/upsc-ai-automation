import os
import feedparser
from datetime import datetime
from supabase import create_client

from sidebar import fetch_quotes, fetch_facts, fetch_reports

from news_sources import RSS_FEEDS
from news_filter import is_relevant
from article_extractor import extract_article
from gs_classifier import classify_gs
from importance import importance


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

                    "title": item.get(
                        "title",
                        ""
                    ),

                    "link": item.get(
                        "link",
                        ""
                    ),

                    "summary": item.get(
                        "summary",
                        item.get(
                            "description",
                            ""
                        )
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

    try:

        result = (
            supabase
            .table("upsc_notes")
            .select("id")
            .eq("title", title)
            .execute()
        )

        return len(result.data) > 0


    except Exception as e:

        print(
            "Duplicate check failed:",
            e
        )

        return False




# -----------------------------
# SAVE ARTICLE
# -----------------------------

def save_article(article, full_text):


    data = {


        "date":
        datetime.now().strftime(
            "%Y-%m-%d"
        ),


        "title":
        article["title"],


        "source":
        article["link"],


        "gs_paper":
        classify_gs(
            article["title"],
            article["summary"]
        ),


        "importance":
        importance(
            article["title"],
            article["summary"]
        ),


        "notes":
        full_text if full_text else article["summary"]

    }



    supabase.table(
        "upsc_notes"
    ).insert(
        data
    ).execute()





# -----------------------------
# MAIN AUTOMATION
# -----------------------------

def main():


    print(
        "Starting UPSC News Automation"
    )


    articles = fetch_news()


    print(
        "Total articles fetched:",
        len(articles)
    )



    saved = 0



    for article in articles:


        title = article["title"]


        if not title:

            continue



        print(
            "\nChecking:",
            title
        )



        # FILTER IRRELEVANT NEWS

        if not is_relevant(
            title,
            article["summary"]
        ):

            print(
                "Skipped - Not relevant"
            )

            continue




        # DUPLICATE CHECK

        if already_exists(title):

            print(
                "Skipped - Duplicate"
            )

            continue





        # ARTICLE EXTRACTION

        print(
            "Extracting article..."
        )


        full_text = extract_article(
            article["link"]
        )



        if not full_text:

            print(
                "Using RSS summary"
            )



        # SAVE

        print(
            "Saving:",
            title
        )


        save_article(
            article,
            full_text
        )


        saved += 1




    # -------------------------
    # SIDEBAR UPDATE
    # -------------------------

    print(
        "\nUpdating UPSC Lens sidebar"
    )


    fetch_quotes(
        supabase
    )


    fetch_facts(
        supabase
    )


    fetch_reports(
        supabase
    )



    print(
        "\nAutomation completed"
    )


    print(
        "New articles saved:",
        saved
    )





if __name__ == "__main__":

    main()
