import feedparser
from datetime import datetime


SOURCES = {

    "PIB":
    "https://pib.gov.in/RssMain.aspx",

    "RBI":
    "https://www.rbi.org.in/rss/PressReleases.xml",

    "ISRO":
    "https://www.isro.gov.in/rss.xml",

    "NITI Aayog":
    "https://www.niti.gov.in/rss.xml"

}


def today():

    return datetime.now().strftime("%Y-%m-%d")



def exists(supabase, table, column, value):

    result = (
        supabase
        .table(table)
        .select("id")
        .eq(column, value)
        .execute()
    )

    return bool(result.data)



def get_subject(text):

    text = text.lower()

    if any(x in text for x in [
        "rbi",
        "inflation",
        "economy",
        "bank",
        "finance"
    ]):
        return "Economy"


    if any(x in text for x in [
        "environment",
        "climate",
        "forest",
        "wildlife"
    ]):
        return "Environment"


    if any(x in text for x in [
        "isro",
        "space",
        "technology",
        "science"
    ]):
        return "Science & Technology"


    if any(x in text for x in [
        "scheme",
        "policy",
        "government",
        "ministry"
    ]):
        return "Governance"


    return "General"



def fetch_live_items():

    items = []


    for source, url in SOURCES.items():

        try:

            feed = feedparser.parse(url)


            for entry in feed.entries[:5]:

                title = entry.get(
                    "title",
                    ""
                )


                summary = entry.get(
                    "summary",
                    ""
                )


                if title:

                    items.append({

                        "source": source,

                        "title": title,

                        "summary": summary

                    })


        except Exception as e:

            print(
                "RSS error",
                source,
                e
            )


    return items



# -----------------------------
# QUOTES
# -----------------------------

def fetch_quotes(supabase):

    quote = {

        "quote":
        "The Constitution is not a mere lawyers' document; it is a vehicle of life.",

        "author":
        "Dr. B.R. Ambedkar",

        "theme":
        "Constitutional Values",

        "date":
        today()

    }


    if not exists(
        supabase,
        "quotes",
        "quote",
        quote["quote"]
    ):

        supabase.table(
            "quotes"
        ).insert(
            quote
        ).execute()



# -----------------------------
# FACTS
# -----------------------------

def fetch_facts(supabase):

    items = fetch_live_items()


    for item in items:


        fact = item["title"]


        if len(fact) < 30:

            continue



        if not exists(
            supabase,
            "daily_facts",
            "fact",
            fact
        ):


            supabase.table(
                "daily_facts"
            ).insert({

                "fact":
                fact,

                "subject":
                get_subject(
                    fact
                ),

                "date":
                today()

            }).execute()



# -----------------------------
# REPORTS
# -----------------------------

def fetch_reports(supabase):

    reports = [

        {
            "report_name":
            "Economic Survey of India",

            "organisation":
            "Ministry of Finance",

            "key_point":
            "Important source for GDP growth, inflation, fiscal deficit and economic reforms."
        },


        {
            "report_name":
            "Monetary Policy Report",

            "organisation":
            "Reserve Bank of India",

            "key_point":
            "Explains inflation outlook and monetary policy decisions."
        }

    ]


    for report in reports:


        if not exists(
            supabase,
            "reports",
            "report_name",
            report["report_name"]
        ):


            report["date"] = today()


            supabase.table(
                "reports"
            ).insert(
                report
            ).execute()
