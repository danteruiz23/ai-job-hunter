"""Fetch a public job posting page and extract main text."""

import os

import requests
import trafilatura

_DEFAULT_TIMEOUT = (
    float(os.getenv("JOB_FETCH_CONNECT_TIMEOUT", "10")),
    float(os.getenv("JOB_FETCH_READ_TIMEOUT", "25")),
)

_MAX_BYTES = int(os.getenv("JOB_FETCH_MAX_BYTES", str(2 * 1024 * 1024)))


def fetch_page_text(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; AIJobHunter/1.0) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    with requests.get(
        url,
        headers=headers,
        timeout=_DEFAULT_TIMEOUT,
        stream=True,
        allow_redirects=True,
    ) as resp:
        resp.raise_for_status()
        ctype = (resp.headers.get("Content-Type") or "").lower()
        if (
            "html" not in ctype
            and "text" not in ctype
            and "xml" not in ctype
        ):
            return ""

        chunks: list[bytes] = []
        total = 0
        for chunk in resp.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > _MAX_BYTES:
                break
            chunks.append(chunk)

    raw = b"".join(chunks)
    if not raw:
        return ""

    html = raw.decode(
        "utf-8",
        errors="replace",
    )
    text = trafilatura.extract(
        html,
        url=url,
        include_comments=False,
        include_tables=True,
        no_fallback=False,
    )
    return (text or "").strip()
