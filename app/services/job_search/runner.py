"""Collect listings from SerpApi, user URLs, and RSS; rank vs candidate."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urldefrag
from urllib.parse import urlparse
from urllib.parse import urlunparse

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator

from app.ai.job_search_params import extract_job_search_params
from app.ai.job_search_ranker import rank_listings_vs_candidate
from app.services.job_search.fetch_job_page import fetch_page_text
from app.services.job_search.rss_reader import fetch_rss_items
from app.services.job_search.serpapi_google_jobs import fetch_google_jobs
from app.services.job_search.url_safety import is_http_url_allowed


_VALID_JOB_TYPES = {"", "remote", "hybrid", "on-site"}


class JobSearchRequest(BaseModel):
    query: str | None = Field(default=None, max_length=400)
    location: str | None = Field(default=None, max_length=200)
    job_type: str | None = Field(default=None, max_length=20)
    job_urls: list[str] = Field(default_factory=list, max_length=35)
    rss_feed_urls: list[str] = Field(default_factory=list, max_length=10)
    num_results: int = Field(default=5, ge=1, le=10)
    serpapi_api_key: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def _normalize_lists(self) -> JobSearchRequest:
        self.job_urls = [
            str(x).strip()
            for x in self.job_urls
            if str(x).strip()
        ][:35]
        self.rss_feed_urls = [
            str(x).strip()
            for x in self.rss_feed_urls
            if str(x).strip()
        ][:10]
        if self.query is not None:
            self.query = self.query.strip() or None
        if self.location is not None:
            self.location = self.location.strip() or None
        if self.job_type is not None:
            self.job_type = self.job_type.strip().lower() or None
            if self.job_type and self.job_type not in _VALID_JOB_TYPES:
                self.job_type = None
        return self


_MAX_LISTINGS = int(os.getenv("JOB_SEARCH_MAX_LISTINGS", "40"))
_MAX_PER_RSS = int(os.getenv("JOB_SEARCH_MAX_PER_RSS", "15"))
_MAX_RANK = int(os.getenv("JOB_SEARCH_MAX_RANK", "20"))
_SERPAPI_KEY = os.getenv("SERPAPI_API_KEY", "").strip()


def normalize_job_url(url: str) -> str:
    raw = (url or "").strip()
    base, _frag = urldefrag(raw)
    p = urlparse(base)
    path = p.path or ""
    if path not in ("", "/") and path.endswith("/"):
        path = path[:-1]
    return urlunparse(
        (
            (p.scheme or "https").lower(),
            (p.netloc or "").lower(),
            path,
            "",
            p.query,
            "",
        )
    ).rstrip("?")


@dataclass
class _Listing:
    lid: str
    title: str
    company: str
    url: str
    snippet: str
    listing_source: str


def _parse_line_urls(raw: str, *, cap: int) -> list[str]:
    out: list[str] = []
    for line in (raw or "").splitlines():
        u = line.strip()
        if not u:
            continue
        if is_http_url_allowed(u):
            out.append(u)
        if len(out) >= cap:
            break
    return out


def run_job_search(
    candidate_data: str,
    body: JobSearchRequest,
) -> dict:
    messages: list[str] = []
    serpapi_used = False

    params = extract_job_search_params(candidate_data)
    base_q = (params.get("search_query") or "").strip()
    extra = (body.query or "").strip()
    q = f"{base_q} {extra}".strip() if extra else base_q
    loc = (body.location or params.get("location") or "").strip()

    if not q:
        q = "jobs"
    if body.job_type:
        q = f"{q} {body.job_type}"

    listings: list[_Listing] = []
    seen: set[str] = set()
    lid_seq = 0

    def add(
        title: str,
        company: str,
        url: str,
        snippet: str,
        listing_source: str,
    ) -> None:
        nonlocal lid_seq
        nu = normalize_job_url(url)
        if not nu or nu in seen:
            return
        seen.add(nu)
        lid = f"j{lid_seq}"
        lid_seq += 1
        listings.append(
            _Listing(
                lid=lid,
                title=title or "Untitled",
                company=company or "",
                url=nu,
                snippet=(snippet or "")[:8000],
                listing_source=listing_source,
            )
        )

    _effective_key = (body.serpapi_api_key or "").strip() or _SERPAPI_KEY
    if _effective_key:
        try:
            serp_rows = fetch_google_jobs(
                q=q,
                location=loc,
                api_key=_effective_key,
                max_results=body.num_results,
            )
            serpapi_used = True
            for row in serp_rows:
                add(
                    row["title"],
                    str(row.get("company") or ""),
                    row["url"],
                    str(row.get("snippet") or ""),
                    "serpapi_google_jobs",
                )
        except Exception as exc:
            err = str(exc)
            if _effective_key:
                err = err.replace(_effective_key, "***")
            messages.append(f"SerpApi Google Jobs failed: {err}")
    else:
        messages.append(
            "SerpApi disabled (set SERPAPI_API_KEY for broad Google Jobs search)."
        )

    for u in body.job_urls:
        u = (u or "").strip()
        if not is_http_url_allowed(u):
            messages.append(f"Skipped blocked or invalid URL: {u[:80]}")
            continue
        try:
            text = fetch_page_text(u)
            title = text.split("\n", 1)[0].strip()[:200] if text else u
            add(
                title or "Job posting",
                "",
                u,
                text[:8000],
                "user_url",
            )
        except Exception as exc:
            messages.append(f"Could not fetch URL: {u[:80]} ({exc})")

    for feed in body.rss_feed_urls:
        feed = (feed or "").strip()
        if not is_http_url_allowed(feed):
            messages.append(f"Skipped blocked or invalid RSS URL: {feed[:80]}")
            continue
        try:
            items = fetch_rss_items(
                feed,
                max_items=_MAX_PER_RSS,
            )
            for it in items:
                link = (it.get("link") or "").strip()
                if not is_http_url_allowed(link):
                    continue
                summary = (it.get("summary") or "").strip()
                title = (it.get("title") or "Untitled").strip()
                try:
                    if summary:
                        snippet = summary
                    else:
                        snippet = fetch_page_text(link)[:8000]
                except Exception:
                    snippet = summary
                add(
                    title,
                    "",
                    link,
                    snippet,
                    "rss",
                )
        except Exception as exc:
            messages.append(f"RSS error ({feed[:60]}…): {exc}")

    if not listings:
        return {
            "results": [],
            "messages": messages,
            "search": {
                "query": q,
                "location": loc,
                "serpapi_used": serpapi_used,
            },
        }

    listings = listings[:_MAX_LISTINGS]

    rank_slice = listings[:_MAX_RANK]

    ranked = rank_listings_vs_candidate(
        candidate_data,
        [
            {
                "id": x.lid,
                "title": x.title,
                "company": x.company,
                "snippet": x.snippet[:1000],
            }
            for x in rank_slice
        ],
    )

    score_by_id = {r["id"]: r for r in ranked}

    rank_ids = {x.lid for x in rank_slice}

    results = []
    for x in listings:
        if x.lid in rank_ids:
            r = score_by_id.get(
                x.lid,
                {},
            )
            score = int(r.get("match_score", 50))
            one_liner = str(r.get("one_liner", "")).strip()
        else:
            score = 50
            one_liner = "Not batch-ranked (listing cap)."

        score = max(0, min(100, score))
        results.append(
            {
                "id": x.lid,
                "title": x.title,
                "company": x.company,
                "url": x.url,
                "source": x.listing_source,
                "match_score": score,
                "one_liner": one_liner,
                "snippet_preview": (x.snippet or "")[:500],
            }
        )

    results.sort(
        key=lambda row: row["match_score"],
        reverse=True,
    )

    return {
        "results": results,
        "messages": messages,
        "search": {
            "query": q,
            "location": loc,
            "serpapi_used": serpapi_used,
        },
    }
