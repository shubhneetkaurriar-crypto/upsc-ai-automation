import feedparser
from datetime import datetime


# -----------------------------
# ETHICS QUOTES SOURCES
# -----------------------------

QUOTE_SOURCES = {

    "UN Values":
    "https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml",

    "Gandhi Archives":
    "https://www.gandhi.gov.in/feed"

}



def fetch_quotes(supabase):

    try:

        for source,url in QUOTE_SOURCES.items():

            feed = feedparser.parse(url)


            if len(feed.entries)==0:
                continue


            item = feed.entries[0]


            data = {

                "quote":
                item.get("title",""),

                "author":
                source,

                "theme":
                "Ethics & Values",

                "date":
                datetime.now().strftime("%Y-%m-%d")

            }


            supabase.table(
                "quotes"
            ).insert(data).execute()


            break


    except Exception as e:

        print(
            "Quotes error:",
            e
        )





# -----------------------------
# PRELIMS FACTS
# -----------------------------


FACT_SOURCES = {

    "PIB":
    "https://pib.gov.in/RssMain.aspx",

    "RBI":
    "https://www.rbi.org.in/rss/PressReleases.xml",

    "ISRO":
    "https://www.isro.gov.in/rss.xml"

}




def fetch_facts(supabase):


    try:


        count = 0


        for source,url in FACT_SOURCES.items():


            feed = feedparser.parse(url)



            for item in feed.entries[:2]:


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



                count += 1



                if count >= 5:
                    return



    except Exception as e:

        print(
            "Facts error:",
            e
        )






# -----------------------------
# REPORTS & INDICES
# -----------------------------



REPORT_SOURCES = {


"NITI Aayog":
"https://www.niti.gov.in/rss.xml",


"World Bank":
"https://www.worldbank.org/en/news/all?format=rss",


"IMF":
"https://www.imf.org/en/News/RSS"


}





def fetch_reports(supabase):


    try:


        saved = 0


        for source,url in REPORT_SOURCES.items():


            feed = feedparser.parse(url)



            for item in feed.entries[:2]:


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



                saved += 1



                if saved >= 5:
                    return




    except Exception as e:

        print(
            "Reports error:",
            e
        )
