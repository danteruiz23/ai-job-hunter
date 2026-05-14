"""Pull recent items from RSS or Atom feeds (stdlib XML)."""

import os
import re
import xml.etree.ElementTree as ET

import requests

_DEFAULT_TIMEOUT = (
    float(os.getenv("JOB_FETCH_CONNECT_TIMEOUT", "10")),
    float(os.getenv("JOB_FETCH_READ_TIMEOUT", "25")),
)

_MAX_FEED_BYTES = int(os.getenv("JOB_RSS_MAX_BYTES", str(3 * 1024 * 1024)))

_NS_STRIP = re.compile(r"\{[^}]+\}")


def _local(tag: str) -> str:
    return _NS_STRIP.sub("", tag)


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return "".join(el.itertext()).strip()


def fetch_rss_items(feed_url: str, *, max_items: int) -> list[dict[str, str]]:
    r = requests.get(
        feed_url,
        timeout=_DEFAULT_TIMEOUT,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; AIJobHunter/1.0) "
                "AppleWebKit/537.36"
            ),
        },
    )
    r.raise_for_status()
    if len(r.content) > _MAX_FEED_BYTES:
        raise ValueError("RSS feed response too large")

    root = ET.fromstring(r.content)
    tag = _local(root.tag).lower()
    items: list[dict[str, str]] = []

    if tag == "rss":
        channel = root.find("channel")
        if channel is None:
            return []
        for it in channel.findall("item"):
            if len(items) >= max_items:
                break
            title = _text(it.find("title"))
            link_el = it.find("link")
            link = _text(link_el)
            summary = _text(it.find("description"))[:4000]
            if link:
                items.append(
                    {
                        "title": title or "Untitled",
                        "link": link,
                        "summary": summary,
                    }
                )
        return items

    if tag == "feed":
        for entry in root:
            if _local(entry.tag).lower() != "entry":
                continue
            if len(items) >= max_items:
                break
            title = ""
            link = ""
            summary = ""
            for child in entry:
                ln = _local(child.tag).lower()
                if ln == "title":
                    title = _text(child)
                elif ln == "link":
                    href = (child.get("href") or "").strip()
                    rel = (child.get("rel") or "alternate").lower()
                    if href and rel in ("alternate", ""):
                        link = href
                elif ln in ("summary", "content"):
                    bit = _text(child)[:4000]
                    if len(bit) > len(summary):
                        summary = bit
            if link:
                items.append(
                    {
                        "title": title or "Untitled",
                        "link": link,
                        "summary": summary,
                    }
                )
        return items

    return []
