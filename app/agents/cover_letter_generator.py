from app.services.openai_service import (
    get_client,
    DEFAULT_MODEL
)

client = get_client()


def generate_cover_letter(
    candidate_profile,
    match_result,
    job_description
):

    prompt = f"""
    You are an elite executive career coach
    and professional cover letter writer.

    Generate a compelling executive-level
    cover letter tailored specifically
    for this role.

    IMPORTANT:

    - Professional executive tone
    - Concise and impactful
    - Maximum 1 page
    - Emphasize telecom leadership
    - Highlight operational impact
    - Mention AI and automation expertise
    - Reference SLA and vendor governance
    - Position candidate strongly
    - Avoid generic language

    CANDIDATE PROFILE:

    {candidate_profile}

    MATCH ANALYSIS:

    {match_result}

    JOB DESCRIPTION:

    {job_description}

    Return ONLY the cover letter.
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

    return response.choices[0].message.content