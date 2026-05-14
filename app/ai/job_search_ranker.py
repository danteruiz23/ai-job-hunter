"""Batch-score job listings against a candidate (single LLM call)."""

from app.ai.openai_client import get_openai_client
from app.services.json_utils import extract_json

_MODEL = "gpt-4.1-mini"


def rank_listings_vs_candidate(
    candidate_data: str,
    listings: list[dict],
) -> list[dict]:
    excerpt = (candidate_data or "").strip()[:12000]

    lines = []
    for row in listings:
        lid = str(row.get("id", "")).strip()
        title = str(row.get("title", "")).strip()
        company = str(row.get("company", "")).strip()
        snippet = str(row.get("snippet", "")).strip()[:900]
        lines.append(
            f"id={lid}\n"
            f"title={title}\n"
            f"company={company}\n"
            f"snippet={snippet}\n"
        )

    blob = "\n---\n".join(lines)

    prompt = f"""
You are an expert recruiter.

Compare the candidate to EACH job listing below.

Return ONLY valid JSON:

{{
  "rankings": [
    {{
      "id": "same id as given",
      "match_score": 0,
      "one_liner": "12-20 words: fit vs gaps"
    }}
  ]
}}

match_score: integer 0-100 for overall fit.

You MUST include one object per listing id exactly once.

CANDIDATE (resume / profile text):

{excerpt}

LISTINGS:

{blob}
"""

    response = get_openai_client().chat.completions.create(
        model=_MODEL,
        temperature=0.15,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    content = response.choices[0].message.content or ""
    data = extract_json(content)
    raw = data.get("rankings") or []

    if not isinstance(raw, list):
        return []

    out: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        lid = str(item.get("id", "")).strip()
        if not lid:
            continue
        try:
            score = int(item.get("match_score", 50))
        except (TypeError, ValueError):
            score = 50
        out.append(
            {
                "id": lid,
                "match_score": score,
                "one_liner": str(item.get("one_liner", "")).strip(),
            }
        )

    known = {str(x.get("id")) for x in listings}
    seen: set[str] = set()
    filtered = []
    for row in out:
        if row["id"] in known and row["id"] not in seen:
            seen.add(row["id"])
            filtered.append(row)

    for row in listings:
        lid = str(row.get("id", "")).strip()
        if lid and lid not in seen:
            filtered.append(
                {
                    "id": lid,
                    "match_score": 50,
                    "one_liner": "Not scored by model.",
                }
            )

    return filtered
