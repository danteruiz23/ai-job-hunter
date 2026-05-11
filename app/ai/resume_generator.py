from openai import OpenAI
from dotenv import load_dotenv
import os

from app.ai.prompt_engine import RESUME_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

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

    response = client.chat.completions.create(
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