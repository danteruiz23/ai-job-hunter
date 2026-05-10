from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_cover_letter(profile, match_analysis, job_description):

    prompt = f"""
Write an executive-level cover letter.

PROFILE:
{profile}

MATCH ANALYSIS:
{match_analysis}

JOB DESCRIPTION:
{job_description}

Requirements:

- strong opening
- leadership tone
- measurable achievements
- concise executive language
- business impact
- AI transformation positioning
- telecom leadership positioning

Avoid generic AI wording.

Make it:
- professional
- persuasive
- modern
- recruiter-ready
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content