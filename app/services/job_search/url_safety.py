"""SSRF-minded URL allowlisting for user-supplied fetch targets."""

import ipaddress
from urllib.parse import urlparse


_LOCAL_HOSTNAMES = frozenset(
    {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "::1",
        "metadata.google.internal",
        "metadata",
    }
)


def is_http_url_allowed(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False

    raw = url.strip()

    if len(raw) > 2048:
        return False

    parsed = urlparse(raw)

    if parsed.scheme not in ("http", "https"):
        return False

    host = (parsed.hostname or "").lower().strip("[]")

    if not host:
        return False

    if host in _LOCAL_HOSTNAMES:
        return False

    if host.endswith(".local") or host.endswith(".localhost"):
        return False

    try:
        ip = ipaddress.ip_address(host)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            return False
    except ValueError:
        pass

    return True
