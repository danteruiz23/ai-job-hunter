def detect_industry(text):

    text = text.lower()

    industries = {

        "software engineering": [
            "python",
            "react",
            "api",
            "backend",
            "frontend",
            "developer",
            "software engineer",
        ],

        "telecommunications": [
            "mpls",
            "carrier",
            "fiber",
            "subsea",
            "telecom",
            "noc",
        ],

        "finance": [
            "banking",
            "investment",
            "financial",
            "forecast",
            "accounting",
        ],

        "marketing": [
            "seo",
            "campaign",
            "growth",
            "social media",
            "branding",
        ],

        "healthcare": [
            "patient",
            "clinical",
            "nurse",
            "medical",
            "hospital",
        ],

        "operations": [
            "operations",
            "process improvement",
            "supply chain",
            "logistics",
        ]
    }

    scores = {}

    for industry, keywords in industries.items():

        scores[industry] = sum(
            1 for keyword in keywords
            if keyword in text
        )

    return max(
        scores,
        key=scores.get
    )