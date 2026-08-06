import feedparser
from datetime import datetime


# -----------------------------
# DAILY QUOTES
# -----------------------------

QUOTE_FEEDS = {

    "Gandhi Archives":
    "https://www.gandhi.gov.in/feed",

    "UN":
    "https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml"

}


def fetch_quotes(supabase):

    for source, url in QUOTE_FEEDS.items():

        try:

            feed = feedparser.parse(url)

            for item in feed.entries[:1]:

                data = {

                    "quote":
                    item.get("title",""),

                    "author":
                    source,

                    "theme":
                    "Ethics",

                    "date":
                    datetime.now().strftime("%Y-%m-%d")

                }


                supabase.table(
                    "quotes"
                ).insert(data).execute()


        except Exception as e:

            print("Quote error:", e)




# -----------------------------
# DAILY FACTS
# -----------------------------

FACT_FEEDS = {

    "PIB":
    "https://pib.gov.in/RssMain.aspx",

    "ISRO":
    "https://www.isro.gov.in/rss.xml",

    "RBI":
    "https://www.rbi.org.in/rss/PressReleases.xml"

}



def fetch_facts(supabase):


    for source,url in FACT_FEEDS.items():

        try:

            feed = feedparser.parse(url)


            for item in feed.entries[:5]:

                data = {

                    "fact":
                    item.get("title",""),

                    "subject":
                    source,

                    "date":
                    datetime.now().strftime("%Y-%m-%d")

                }


                supabase.table(
                    "daily_facts"
                ).insert(data).execute()



        except Exception as e:

            print(
                "Fact error:",
                e
            )





# -----------------------------
# REPORTS & INDICES
# -----------------------------


REPORT_FEEDS = {


    "NITI Aayog":
    "https://www.niti.gov.in/rss.xml",


    "World Bank":
    "https://www.worldbank.org/en/news/all?format=rss"

}




def fetch_reports(supabase):


    for source,url in REPORT_FEEDS.items():

        try:

            feed = feedparser.parse(url)


            for item in feed.entries[:3]:


                data = {


                    "report_name":
                    item.get("title",""),


                    "organisation":
                    source,


                    "key_point":
                    item.get(
                        "summary",
                        ""
                    ),


                    "date":
                    datetime.now().strftime("%Y-%m-%d")

                }



                supabase.table(
                    "reports"
                ).insert(data).execute()



        except Exception as e:

            print(
                "Report error:",
                e
            )
