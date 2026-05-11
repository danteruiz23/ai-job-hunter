from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from app.ai.prompt_engine import MATCH_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

_JSON_RETRY_REMINDER = """
Return ONLY valid JSON that matches the required schema.
No markdown, no code fences, no additional commentary.
""".strip()

def _coerce_match_json(text: str):

    if not text:
        raise ValueError("Empty model response")

    text = text.strip()

    # If the model accidentally includes extra text, try to extract the first JSON object.
    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]

    data = json.loads(text)

    analysis = str(data.get("analysis", "")).strip()
    match_score = int(data.get("match_score", 0))
    ats_score = int(data.get("ats_score", 0))
    missing_skills = data.get("missing_skills", [])

    if not isinstance(missing_skills, list):
        missing_skills = []

    missing_skills = [
        str(s).strip()
        for s in missing_skills
        if str(s).strip()
    ][:15]

    match_score = max(0, min(100, match_score))
    ats_score = max(0, min(100, ats_score))

    return {
        "analysis": analysis,
        "match_score": match_score,
        "ats_score": ats_score,
        "missing_skills": missing_skills,
    }

def _call_match_model(
    prompt: str,
    *,
    temperature: float,
):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": MATCH_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.choices[0].message.content

def generate_match_analysis(
    candidate_data,
    job_description
):

    prompt = f"""
CANDIDATE PROFILE:

{candidate_data}


JOB DESCRIPTION:

{job_description}
"""

    # Attempt 1: normal generation
    content = _call_match_model(
        prompt,
        temperature=0.7,
    )

    try:
        return _coerce_match_json(content)
    except Exception:
        # Attempt 2: strict JSON reminder, lower temperature
        retry_content = _call_match_model(
            f"{prompt}\n\n{_JSON_RETRY_REMINDER}",
            temperature=0.0,
        )
        return _coerce_match_json(retry_content)