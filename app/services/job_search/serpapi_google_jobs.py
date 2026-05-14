"""SerpApi Google Jobs engine (optional; requires SERPAPI_API_KEY)."""

import os
from typing import Any

import requests

_SERP_TIMEOUT = (
    float(os.getenv("JOB_FETCH_CONNECT_TIMEOUT", "10")),
    float(os.getenv("JOB_FETCH_READ_TIMEOUT", "40")),
)


def fetch_google_jobs(
    *,
    q: str,
    location: str,
    api_key: str,
    max_results: int,
) -> list[dict[str, Any]]:
    params: dict[str, str | int] = {
        "engine": "google_jobs",
        "q": q,
        "hl": "en",
        "api_key": api_key,
    }
    loc = (location or "").strip()
    if loc:
        params["location"] = loc

    r = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=_SERP_TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()

    jobs = data.get("jobs_results") or []
    out: list[dict[str, Any]] = []

    for row in jobs:
        if len(out) >= max_results:
            break
        title = (row.get("title") or "").strip()
        company = (row.get("company_name") or "").strip()
        locs = row.get("location") or row.get("locations") or ""
        if isinstance(locs, list):
            loc_str = ", ".join(str(x) for x in locs[:3])
        else:
            loc_str = str(locs).strip()

        desc = (row.get("description") or "").strip()
        apply_options = row.get("apply_options") or []
        url = ""
        if isinstance(apply_options, list) and apply_options:
            first = apply_options[0]
            if isinstance(first, dict):
                url = (first.get("link") or "").strip()
        if not url and row.get("share_link"):
            url = str(row.get("share_link")).strip()

        if not title or not url:
            continue

        snippet = desc[:6000] if desc else ""
        out.append(
            {
                "title": title,
                "company": company,
                "location": loc_str,
                "url": url,
                "snippet": snippet,
                "source": "serpapi_google_jobs",
            }
        )

    return out
