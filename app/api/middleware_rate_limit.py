import os
import time
import asyncio
from collections import defaultdict
from collections import deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


def _truthy(
    raw: str,
) -> bool:

    return raw.strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


def _client_key(
    request: Request,
) -> str:

    api_key = (
        request.headers.get(
            "x-api-key",
            "",
        )
        or request.headers.get(
            "X-Api-Key",
            "",
        )
    ).strip()

    if api_key:

        return f"k:{hash(api_key)}"

    forwarded = request.headers.get(
        "x-forwarded-for",
        "",
    )

    if forwarded:

        return forwarded.split(
            ",",
        )[0].strip()

    if request.client:

        return request.client.host

    return "unknown"


def _bucket_for_path(
    path: str,
) -> str | None:

    if path in (
        "/",
        "/health",
    ):

        return None

    for prefix in (
        "/docs",
        "/redoc",
        "/openapi.json",
    ):

        if path.startswith(prefix):

            return None

    if path.startswith(
        "/upload-",
    ):

        return "upload"

    if path in (
        "/profile",
        "/match",
        "/resume",
        "/cover-letter",
        "/job-search",
    ):

        return "ai"

    return "default"


class RateLimitMiddleware(BaseHTTPMiddleware):

    """Sliding-window request cap per client (API key if present, else IP)."""

    def __init__(
        self,
        app,
    ):

        super().__init__(app)

        self._disabled = _truthy(
            os.getenv(
                "RATE_LIMIT_DISABLED",
                "",
            ),
        )

        self._window = float(
            os.getenv(
                "RATE_LIMIT_WINDOW_SEC",
                "60",
            ),
        )

        self._max_default = int(
            os.getenv(
                "RATE_LIMIT_DEFAULT",
                "120",
            ),
        )

        self._max_upload = int(
            os.getenv(
                "RATE_LIMIT_UPLOAD",
                "30",
            ),
        )

        self._max_ai = int(
            os.getenv(
                "RATE_LIMIT_AI",
                "20",
            ),
        )

        self._lock = asyncio.Lock()

        self._hits: dict[
            tuple[str, str],
            deque[float],
        ] = defaultdict(deque)

    def _max_for_bucket(
        self,
        bucket: str,
    ) -> int:

        if bucket == "upload":

            return self._max_upload

        if bucket == "ai":

            return self._max_ai

        return self._max_default

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        if self._disabled:

            return await call_next(request)

        if request.method == "OPTIONS":

            return await call_next(request)

        bucket = _bucket_for_path(
            request.url.path,
        )

        if bucket is None:

            return await call_next(request)

        key = _client_key(request)

        dq_key = (
            key,
            bucket,
        )

        now = time.monotonic()

        cutoff = now - self._window

        max_req = self._max_for_bucket(bucket)

        async with self._lock:

            dq = self._hits[dq_key]

            while dq and dq[0] < cutoff:

                dq.popleft()

            if len(dq) >= max_req:

                return JSONResponse(
                    {
                        "detail": (
                            "Rate limit exceeded. "
                            "Slow down and try again shortly."
                        ),
                    },
                    status_code=429,
                    headers={
                        "Retry-After": str(
                            max(
                                1,
                                int(self._window),
                            ),
                        ),
                    },
                )

            dq.append(now)

        return await call_next(request)
