from dotenv import load_dotenv

from app.ai.openai_client import get_openai_client
from app.ai.prompt_engine import RESUME_PROMPT

load_dotenv()


def generate_resume(
    candidate_data,
    job_description
):

    prompt = f"""
CANDIDATE PROFILE:

{candidate_data}


TARGET JOB DESCRIPTION:

{job_description}


Generate a premium ATS-optimized executive resume tailored specifically for this role.
"""

    response = get_openai_client().chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": RESUME_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    resume = response.choices[0].message.content

    return resume