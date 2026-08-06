IRRELEVANT_KEYWORDS = [
    "cricket",
    "ipl",
    "football",
    "cinema",
    "movie",
    "actor",
    "actress",
    "celebrity",
    "entertainment",
    "fashion",
    "music",
    "murder",
    "rape",
    "accident",
    "lottery",
    "viral",
    "youtube",
    "instagram",
    "tiktok",
    "wedding",
    "weather forecast"
]


IMPORTANT_KEYWORDS = [
    "parliament",
    "bill",
    "act",
    "supreme court",
    "high court",
    "constitution",
    "government",
    "cabinet",
    "scheme",
    "policy",
    "economy",
    "inflation",
    "gdp",
    "rbi",
    "bank",
    "environment",
    "climate",
    "forest",
    "wildlife",
    "biodiversity",
    "isro",
    "space",
    "science",
    "technology",
    "artificial intelligence",
    "health",
    "education",
    "agriculture",
    "international",
    "un",
    "india",
    "g20",
    "brics",
    "imf",
    "world bank",
    "wto",
    "unesco",
    "cop",
    "election commission",
    "cag",
    "niti aayog"
]


def is_relevant(title, summary=""):

    text = (title + " " + summary).lower()

    for word in IRRELEVANT_KEYWORDS:
        if word in text:
            return False

    for word in IMPORTANT_KEYWORDS:
        if word in text:
            return True

    return False
