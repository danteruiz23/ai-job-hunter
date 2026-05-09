from app.services.openai_service import (
    get_client,
    DEFAULT_MODEL
)

from app.services.json_utils import (
    extract_json
)

client = get_client()


def extract_candidate_data(profile_text):

    prompt = f"""
    Analyze this combined professional profile.

    Extract and return ONLY valid JSON.

    Required fields:

    {{
        "full_name": "",
        "current_title": "",
        "years_experience": "",
        "leadership_level": "",
        "industries": [],
        "skills": [],
        "certifications": [],
        "languages": [],
        "ai_experience": "",
        "telecom_experience": "",
        "management_experience": "",
        "summary": ""
    }}

    PROFILE:

    {profile_text}
    """

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    return extract_json(content)