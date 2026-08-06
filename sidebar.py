import feedparser
from datetime import datetime


# -----------------------------
# SOURCES
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

def exists(supabase, table, column, value):

    result = (
        supabase
        .table(table)
        .select("id")
        .eq(column, value)
        .execute()
    )

    return len(result.data) > 0




# -----------------------------
# SUBJECT CLASSIFICATION
# -----------------------------

def classify_subject(text):

    text = text.lower()


    if any(x in text for x in [
        "economy",
        "rbi",
        "bank",
        "inflation",
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
        "space",
        "isro",
        "satellite",
        "technology"
    ]):
        return "Science & Technology"


    if any(x in text for x in [
        "policy",
        "scheme",
        "government",
        "governance"
    ]):
        return "Governance"


    return "General"




# -----------------------------
# FETCH RSS
# -----------------------------

def fetch_online_updates():

    items = []


    for source, url in SOURCES.items():

        try:

            feed = feedparser.parse(url)


            for entry in feed.entries[:5]:

                items.append({

                    "source": source,

                    "title": entry.get(
                        "title",
                        ""
                    ),

                    "summary": entry.get(
                        "summary",
                        ""
                    )

                })


        except Exception as e:

            print(
                source,
                "failed:",
                e
            )


    return items




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
            "Constitutionalism"
        },

        {
            "quote":
            "The best way to find yourself is to lose yourself in the service of others.",
            "author":
            "Mahatma Gandhi",
            "theme":
            "Public Service"
        }

    ]


    for q in quotes:

        if not exists(
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

    updates = fetch_online_updates()


    for item in updates:


        fact = item["title"]


        if len(fact) < 20:

            continue



        if not exists(
            supabase,
            "daily_facts",
            "fact",
            fact
        ):


            data = {

                "fact":
                fact,

                "subject":
                classify_subject(
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
            "RBI Monetary Policy Report",

            "organisation":
            "Reserve Bank of India",

            "key_point":
            "Important for inflation, monetary policy and banking sector analysis."
        },


        {
            "report_name":
            "Economic Survey of India",

            "organisation":
            "Ministry of Finance",

            "key_point":
            "Provides analysis of India's economic performance."
        },


        {
            "report_name":
            "Human Development Report",

            "organisation":
            "UNDP",

            "key_point":
            "Important for social development indicators."
        }

    ]


    for report in reports:


        if not exists(
            supabase,
            "reports",
            "report_name",
            report["report_name"]
        ):


            report["date"] = datetime.now().strftime(
                "%Y-%m-%d"
            )


            supabase.table(
                "reports"
            ).insert(report).execute()
