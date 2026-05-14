"""Derive broad job-search parameters from resume + LinkedIn text."""

from app.ai.openai_client import get_openai_client
from app.services.json_utils import extract_json

_MODEL = "gpt-4.1-mini"


def extract_job_search_params(candidate_data: str) -> dict:
    text = (candidate_data or "").strip()
    if not text:
        return {
            "search_query": "",
            "location": "",
        }

    excerpt = text[:24000]

    prompt = f"""
You help a job seeker run a web job search.

Read the candidate documents and return ONLY valid JSON with this shape:

{{
  "search_query": "short job title + 2-5 key skills for a search box",
  "location": "city, region/country or empty if unknown"
}}

Rules:
- search_query: English, no employer names, under 120 characters.
- location: empty string if not inferable.

CANDIDATE DOCUMENTS:

{excerpt}
"""

    response = get_openai_client().chat.completions.create(
        model=_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    content = response.choices[0].message.content or ""
    data = extract_json(content)

    return {
        "search_query": str(data.get("search_query", "")).strip()[:200],
        "location": str(data.get("location", "")).strip()[:200],
    }
