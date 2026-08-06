IRRELEVANT_KEYWORDS = [

    # Sports
    "cricket",
    "ipl",
    "football",

    # Entertainment
    "cinema",
    "movie",
    "actor",
    "actress",
    "celebrity",
    "entertainment",
    "fashion",
    "music",

    # Lifestyle / Viral
    "wedding",
    "viral",
    "instagram",
    "youtube",
    "tiktok",
    "influencer",

    # Crime / Local news
    "murder",
    "rape",
    "accident",
    "robbery",
    "theft",

    # Commercial news
    "mobile launch",
    "smartphone",
    "iphone",
    "android",
    "laptop",
    "gadget",
    "product launch",
    "car launch",
    "bike launch",
    "automobile",

    # Weather
    "weather forecast",
    "rain alert",
    "temperature"
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
    "budget",

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

    text = (
        title + " " + summary
    ).lower()


    # Reject commercial/news noise first
    for word in IRRELEVANT_KEYWORDS:

        if word in text:
            return False


    # Accept UPSC relevant topics
    for word in IMPORTANT_KEYWORDS:

        if word in text:
            return True


    return False
