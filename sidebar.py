from datetime import date


def fetch_quotes(supabase):

    quotes = [
        {
            "quote": "The best way to predict the future is to create it.",
            "author": "Abraham Lincoln",
            "theme": "Ethics",
            "date": str(date.today())
        }
    ]

    for q in quotes:
        supabase.table("quotes").insert(q).execute()



def fetch_facts(supabase):

    facts = [
        {
            "fact": "India is the world's largest democracy.",
            "subject": "Polity",
            "date": str(date.today())
        },
        {
            "fact": "ISRO is India's space agency.",
            "subject": "Science",
            "date": str(date.today())
        }
    ]

    for f in facts:
        supabase.table("daily_facts").insert(f).execute()



def fetch_reports(supabase):

    reports = [
        {
            "report_name": "Human Development Report",
            "organisation": "UNDP",
            "key_point": "Tracks human development indicators.",
            "date": str(date.today())
        }
    ]

    for r in reports:
        supabase.table("reports").insert(r).execute()
