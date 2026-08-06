GS_RULES = {

    "GS1": [
        "history",
        "culture",
        "heritage",
        "art",
        "dance",
        "festival",
        "archaeology",
        "unesco"
    ],

    "GS2": [
        "constitution",
        "supreme court",
        "high court",
        "parliament",
        "bill",
        "act",
        "government",
        "cabinet",
        "scheme",
        "governor",
        "president",
        "election commission",
        "judiciary",
        "policy"
    ],

    "GS3 Economy": [
        "economy",
        "gdp",
        "inflation",
        "repo",
        "rbi",
        "bank",
        "finance",
        "budget",
        "tax",
        "investment"
    ],

    "GS3 Environment": [
        "environment",
        "climate",
        "forest",
        "wildlife",
        "biodiversity",
        "pollution",
        "cop",
        "wetland"
    ],

    "GS3 Science": [
        "science",
        "technology",
        "space",
        "isro",
        "satellite",
        "ai",
        "artificial intelligence",
        "quantum",
        "semiconductor"
    ],

    "GS4": [
        "ethics",
        "integrity",
        "transparency",
        "accountability"
    ]
}


def classify_gs(title, summary=""):

    text = (title + " " + summary).lower()

    for gs, words in GS_RULES.items():

        for word in words:

            if word in text:
                return gs

    return "GS2"
