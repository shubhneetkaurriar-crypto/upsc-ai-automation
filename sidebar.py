import feedparser
from datetime import datetime


RSS_SOURCES = {

    "PIB":
    "https://pib.gov.in/RssMain.aspx",

    "RBI":
    "https://www.rbi.org.in/rss/PressReleases.xml",

    "The Hindu Science":
    "https://www.thehindu.com/sci-tech/feeder/default.rss",

    "Indian Express":
    "https://indianexpress.com/section/india/feed/"

}



def today():

    return datetime.now().strftime("%Y-%m-%d")



def check_exists(supabase, table, column, value):

    result = (
        supabase
        .table(table)
        .select("id")
        .eq(column, value)
        .execute()
    )

    return len(result.data) > 0




def find_subject(text):

    text = text.lower()


    if any(word in text for word in [
        "rbi",
        "inflation",
        "economy",
        "bank",
        "finance"
    ]):
        return "Economy"


    if any(word in text for word in [
        "climate",
        "forest",
        "wildlife",
        "environment"
    ]):
        return "Environment"


    if any(word in text for word in [
        "science",
        "technology",
        "space",
        "isro"
    ]):
        return "Science & Technology"


    if any(word in text for word in [
        "government",
        "scheme",
        "policy",
        "court",
        "parliament"
    ]):
        return "Polity"


    return "General"




def get_live_news():

    articles = []


    for source, url in RSS_SOURCES.items():

        feed = feedparser.parse(url)


        for item in feed.entries[:5]:

            title = item.get("title", "")


            if title:

                articles.append({

                    "title": title,

                    "source": source

                })


    return articles




def fetch_quotes(supabase):

    data = {

        "quote":
        "The Constitution is not a mere lawyers' document; it is a vehicle of life.",

        "author":
        "Dr. B.R. Ambedkar",

        "theme":
        "Constitutional Values",

        "date":
        today()

    }


    if not check_exists(
        supabase,
        "quotes",
        "quote",
        data["quote"]
    ):

        supabase.table(
            "quotes"
        ).insert(data).execute()




def fetch_facts(supabase):

    news = get_live_news()


    print("FACTS FOUND:", len(news))


    for item in news:


        if not check_exists(
            supabase,
            "daily_facts",
            "fact",
            item["title"]
        ):


            supabase.table(
                "daily_facts"
            ).insert({

                "fact":
                item["title"],

                "subject":
                find_subject(
                    item["title"]
                ),

                "date":
                today()

            }).execute()




def fetch_reports(supabase):

    reports = [

        {
            "report_name":
            "Economic Survey of India",

            "organisation":
            "Ministry of Finance",

            "key_point":
            "Important for economic growth, inflation and fiscal policy."
        },

        {
            "report_name":
            "World Development Report",

            "organisation":
            "World Bank",

            "key_point":
            "Important for development indicators and policy analysis."
        }

    ]


    for report in reports:


        if not check_exists(
            supabase,
            "reports",
            "report_name",
            report["report_name"]
        ):

            report["date"] = today()


            supabase.table(
                "reports"
            ).insert(report).execute()
