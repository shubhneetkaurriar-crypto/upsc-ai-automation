import feedparser
from datetime import datetime


# -----------------------------
# LIVE SOURCES
# -----------------------------

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



# -----------------------------
# DUPLICATE CHECK
# -----------------------------

def already_exists(supabase, table, column, value):

    result = (
        supabase
        .table(table)
        .select("id")
        .eq(column, value)
        .execute()
    )

    return len(result.data) > 0




# -----------------------------
# SUBJECT CLASSIFIER
# -----------------------------

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
        "wildlife",
        "biodiversity"
    ]):
        return "Environment"


    if any(x in text for x in [
        "isro",
        "space",
        "technology",
        "satellite",
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




# -----------------------------
# FETCH ONLINE NEWS
# -----------------------------

def fetch_updates():

    data = []


    for source, url in SOURCES.items():

        try:

            feed = feedparser.parse(url)


            for item in feed.entries[:5]:

                title = item.get(
                    "title",
                    ""
                )


                summary = item.get(
                    "summary",
                    ""
                )


                if title:

                    data.append({

                        "source": source,

                        "title": title,

                        "summary": summary

                    })


        except Exception as e:

            print(
                source,
                e
            )


    return data




# -----------------------------
# QUOTES
# -----------------------------

def fetch_quotes(supabase):

    quotes = [

        {
            "quote":
            "The Constitution is not a mere lawyers' document; it is a vehicle of life.",

            "author":
            "Dr. B.R. Ambedkar",

            "theme":
            "Constitutional Values"
        },

        {
            "quote":
            "A public servant must have integrity, empathy and commitment towards citizens.",

            "author":
            "UPSC Ethics Principle",

            "theme":
            "Public Service"
        }

    ]


    for q in quotes:

        if not already_exists(
            supabase,
            "quotes",
            "quote",
            q["quote"]
        ):

            q["date"] = datetime.now().strftime(
                "%Y-%m-%d"
            )

            supabase.table(
                "quotes"
            ).insert(q).execute()




# -----------------------------
# DAILY FACTS
# -----------------------------

def fetch_facts(supabase):

    updates = fetch_updates()


    for item in updates:


        fact = item["title"]


        if len(fact) < 30:

            continue



        if not already_exists(
            supabase,
            "daily_facts",
            "fact",
            fact
        ):


            data = {

                "fact":
                fact,

                "subject":
                get_subject(
                    fact
                ),

                "date":
                datetime.now().strftime(
                    "%Y-%m-%d"
                )

            }


            supabase.table(
                "daily_facts"
            ).insert(data).execute()




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
            "Useful for understanding inflation targeting, repo rate and monetary policy."
        },


        {
            "report_name":
            "Human Development Report",

            "organisation":
            "UNDP",

            "key_point":
            "Provides indicators related to health, education and standard of living."
        }

    ]


    for r in reports:


        if not already_exists(
            supabase,
            "reports",
            "report_name",
            r["report_name"]
        ):


            r["date"] = datetime.now().strftime(
                "%Y-%m-%d"
            )


            supabase.table(
                "reports"
            ).insert(r).execute()
