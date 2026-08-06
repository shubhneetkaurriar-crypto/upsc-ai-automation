IMPORTANT_KEYWORDS = {

    5: [
        "supreme court",
        "constitution",
        "constitutional",
        "parliament",
        "bill",
        "act",
        "budget",
        "economic survey",
        "rbi",
        "repo",
        "inflation",
        "g20",
        "brics",
        "cop",
        "unsc",
        "india-us",
        "india-china",
        "isro"
    ],

    4: [
        "scheme",
        "policy",
        "cabinet",
        "environment",
        "climate",
        "biodiversity",
        "forest",
        "wildlife",
        "technology",
        "artificial intelligence",
        "quantum",
        "semiconductor"
    ],

    3: [
        "education",
        "health",
        "agriculture",
        "economy",
        "bank",
        "science",
        "space",
        "culture",
        "history"
    ]
}


def importance(title, summary=""):

    text = (title + " " + summary).lower()

    for score in [5, 4, 3]:

        for word in IMPORTANT_KEYWORDS[score]:

            if word in text:
                return score

    return 2
