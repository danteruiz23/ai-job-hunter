from app.services.openai_service import (
    get_client,
    DEFAULT_MODEL,
)
from app.services.json_utils import extract_json


def match_candidate_to_job(
    candidate_profile,
    job_description,
):

    client = get_client()

    prompt = f"""
    You are an expert AI recruiter.

    Analyze compatibility between the candidate
    and the job description.

    Return ONLY valid JSON.

    {{
        "match_score": 0,
        "strengths": [],
        "missing_skills": [],
        "recommendations": [],
        "executive_summary": ""
    }}

    CANDIDATE PROFILE:

    {candidate_profile}

    JOB DESCRIPTION:

    {job_description}
    """

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    content = response.choices[0].message.content

    return extract_json(content)
