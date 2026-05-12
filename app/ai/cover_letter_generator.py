from dotenv import load_dotenv

from app.ai.openai_client import get_openai_client
from app.ai.prompt_engine import COVER_LETTER_PROMPT

load_dotenv()


def generate_cover_letter(
    candidate_data,
    job_description
):

    prompt = f"""
CANDIDATE PROFILE:

{candidate_data}


TARGET JOB DESCRIPTION:

{job_description}


Generate a premium executive-level personalized cover letter tailored for this opportunity.
"""

    response = get_openai_client().chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": COVER_LETTER_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    cover_letter = response.choices[0].message.content

    return cover_letter