GS_RULES = {

    "GS1": [
        "history",
        "ancient history",
        "medieval history",
        "modern history",
        "culture",
        "heritage",
        "art",
        "dance",
        "festival",
        "archaeology",
        "unesco",
        "architecture",
        "painting",
        "literature",
        "temple",
        "monument"
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
        "policy",
        "fundamental rights",
        "directive principles",
        "federalism",
        "centre state",
        "local government",
        "panchayat",
        "municipality",
        "governance",
        "public administration",
        "welfare",
        "social justice",
        "health policy",
        "education policy",
        "international relations",
        "foreign policy",
        "united nations",
        "bilateral",
        "diplomatic"
    ],

    "GS3": [
        # Economy
        "economy",
        "economic",
        "gdp",
        "inflation",
        "repo",
        "rbi",
        "bank",
        "banking",
        "finance",
        "budget",
        "tax",
        "taxation",
        "investment",
        "fiscal",
        "monetary",
        "unemployment",
        "employment",
        "manufacturing",
        "industry",
        "exports",
        "imports",
        "trade",
        "agriculture",
        "farmer",
        "farmers",
        "crop",
        "irrigation",
        "msme",

        # Environment
        "environment",
        "climate",
        "forest",
        "wildlife",
        "biodiversity",
        "pollution",
        "cop",
        "wetland",
        "conservation",
        "ecosystem",
        "species",
        "national park",
        "tiger reserve",
        "biosphere reserve",
        "carbon",
        "greenhouse gas",
        "renewable energy",
        "solar energy",
        "wind energy",
        "emissions",

        # Science & Technology
        "science",
        "technology",
        "space",
        "isro",
        "satellite",
        "ai",
        "artificial intelligence",
        "quantum",
        "semiconductor",
        "robotics",
        "biotechnology",
        "genome",
        "genetic",
        "nanotechnology",
        "nuclear",
        "missile",
        "drone",
        "cybersecurity",
        "5g",
        "6g"
    ],

    "GS4": [
        "ethics",
        "integrity",
        "transparency",
        "accountability",
        "probity",
        "emotional intelligence",
        "moral",
        "morality",
        "ethical",
        "civil service values",
        "code of conduct",
        "corruption"
    ]
}


def classify_gs(title, summary=""):

    text = (title + " " + summary).lower()


    for gs, words in GS_RULES.items():

        for word in words:

            if word in text:

                return gs


    # Default category
    return "GS2"
