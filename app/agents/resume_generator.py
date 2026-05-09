from app.services.openai_service import (
    get_client,
    DEFAULT_MODEL
)

client = get_client()


def generate_resume(
    candidate_profile,
    match_result,
    job_description
):

    prompt = f"""
    You are an elite executive resume writer
    and ATS optimization specialist.

    Your task is to generate a highly optimized
    executive-level resume tailored specifically
    for the provided job description.

    IMPORTANT RULES:
IMPORTANT RULES:

- Maintain truthful experience
- Emphasize the candidate's strengths
- Improve ATS keyword density naturally
- Address missing skills strategically
- Highlight leadership and business impact
- Optimize for telecom enterprise leadership roles
- Use a clean executive tone
- Include measurable achievements
- Improve executive summary
- Emphasize SLA, governance, vendors,
  infrastructure, automation and AI
- Make the candidate highly competitive
- Maximum 2 pages
- Keep content concise and executive-focused
- Avoid redundancy
- Prioritize the most relevant achievements
- Use compact bullet points
- Limit each role to the most impactful accomplishments
- Optimize for executive ATS readability
- Do not generate overly detailed case studies
- Target approximately 900-1200 words maximum

    CANDIDATE PROFILE:

    {candidate_profile}

    MATCH ANALYSIS:

    {match_result}

    JOB DESCRIPTION:

    {job_description}

    Return ONLY the optimized resume.
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