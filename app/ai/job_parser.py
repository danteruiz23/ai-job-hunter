import re

COMMON_ROLES = [

    "Software Engineer",
    "Cloud Engineer",
    "Cybersecurity Engineer",
    "Operations Manager",
    "Director of Operations",
    "Project Manager",
    "Data Analyst",
    "Marketing Manager",
    "Sales Manager",
    "Financial Analyst",
    "Product Manager",
    "AI Engineer",
    "Network Engineer",
    "Service Delivery Manager",
]

def extract_target_role(job_description):

    for role in COMMON_ROLES:

        if role.lower() in job_description.lower():

            return role

    # fallback using regex

    patterns = [

        r"position[:\- ]+(.*)",
        r"role[:\- ]+(.*)",
        r"title[:\- ]+(.*)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            job_description,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return "Professional Role"