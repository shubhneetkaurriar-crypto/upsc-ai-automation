import os
import requests
import feedparser
from datetime import datetime
from supabase import create_client


# ==============================
# ENVIRONMENT VARIABLES
# ==============================

GROK_API_KEY = os.environ.get("GROK_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


if not GROK_API_KEY:
    raise Exception("GROK_API_KEY missing")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials missing")


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==============================
# FETCH GOOGLE NEWS
# ==============================

def fetch_news():

    url = (
        "https://news.google.com/rss/search?"
        "q=India+UPSC+OR+government+OR+economy+OR+environment+OR+international+relations"
        "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    articles = []

    for item in feed.entries[:5]:
        articles.append({
            "title": item.title,
            "link": item.link
        })

    return articles



# ==============================
# GROK SUMMARY
# ==============================

def generate_notes(title):

    prompt = f"""
You are a UPSC Civil Services current affairs expert.

Analyze this news:

{title}

Return ONLY in this structure:

GS Paper:
(mention GS1/GS2/GS3/GS4)

Importance:
(number from 1 to 5)

Notes:
- Why in news
- Background
- Key facts for Prelims
- Mains answer points
- Important keywords
"""

    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "grok-4",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    return data["choices"][0]["message"]["content"]



# ==============================
# SAVE TO SUPABASE
# ==============================

def save_to_database(article, notes):

    today = datetime.now().strftime("%Y-%m-%d")

    record = {
        "date": today,
        "title": article["title"],
        "source": article["link"],
        "gs_paper": extract_gs(notes),
        "importance": extract_importance(notes),
        "notes": notes
    }

    supabase.table("upsc_notes").insert(record).execute()



def extract_gs(text):

    for line in text.split("\n"):
        if "GS Paper:" in line:
            return line.replace("GS Paper:", "").strip()

    return "GS2"



def extract_importance(text):

    for line in text.split("\n"):
        if "Importance:" in line:
            try:
                return int(
                    line.replace("Importance:", "")
                    .strip()
                )
            except:
                return 3

    return 3



# ==============================
# MAIN
# ==============================

def main():

    print("Fetching news...")

    articles = fetch_news()

    print(f"Found {len(articles)} articles")

    for article in articles:

        print("Processing:", article["title"])

        notes = generate_notes(
            article["title"]
        )

        save_to_database(
            article,
            notes
        )

        print("Saved successfully")


if __name__ == "__main__":
    main()
