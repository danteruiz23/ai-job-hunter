ADVANCED_SKILLS = {

    # ==================================================
    # BUSINESS / OPERATIONS
    # ==================================================

    "P&L Management": [
        "p&l",
        "profit and loss",
        "financial ownership",
    ],

    "Cost Optimization": [
        "cost optimization",
        "cost reduction",
        "cost savings",
    ],

    "Revenue Growth": [
        "revenue growth",
        "revenue activation",
        "commercial growth",
    ],

    "Order-to-Cash": [
        "order-to-cash",
        "otc lifecycle",
        "billing readiness",
    ],

    "Commercial Contracting": [
        "commercial contracting",
        "enterprise contracting",
        "wholesale contracting",
    ],

    "Operations Management": [
        "operations",
        "operational excellence",
        "service delivery",
    ],

    "Vendor Management": [
        "vendor management",
        "supplier management",
        "partner management",
    ],

    "Program Management": [
        "program management",
        "project management",
    ],

    "Leadership": [
        "leadership",
        "executive leadership",
        "team leadership",
    ],

    "Regional Leadership": [
        "regional leadership",
        "multi-country",
        "latin america",
        "global operations",
    ],

    # ==================================================
    # TECH
    # ==================================================

    "Python": [
        "python",
    ],

    "Cloud": [
        "aws",
        "azure",
        "gcp",
        "cloud",
    ],

    "AI": [
        "artificial intelligence",
        "machine learning",
        "ai",
        "automation",
    ],

    "Cybersecurity": [
        "cybersecurity",
        "security operations",
    ],

    "Data Analysis": [
        "data analysis",
        "analytics",
        "sql",
        "power bi",
    ],

    # ==================================================
    # SALES / MARKETING
    # ==================================================

    "Sales": [
        "sales",
        "business development",
    ],

    "Marketing": [
        "marketing",
        "branding",
        "campaign",
        "seo",
    ],

    # ==================================================
    # FINANCE
    # ==================================================

    "Financial Planning": [
        "forecasting",
        "budgeting",
        "financial planning",
    ],

    # ==================================================
    # HEALTHCARE
    # ==================================================

    "Healthcare Operations": [
        "clinical operations",
        "patient care",
        "healthcare operations",
    ],
}

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for canonical_skill, keywords in ADVANCED_SKILLS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                found_skills.append(
                    canonical_skill
                )

                break

    return list(set(found_skills))