import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class ApiKeyMiddleware(BaseHTTPMiddleware):

    PUBLIC_PREFIXES = (
        "/docs",
        "/redoc",
        "/openapi.json",
    )

    PUBLIC_PATHS = frozenset({
        "/",
        "/health",
    })

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        secret = (
            os.getenv(
                "JOB_HUNTER_API_KEY",
                "",
            ).strip()
        )

        if not secret:

            return await call_next(request)

        if request.method == "OPTIONS":

            return await call_next(request)

        path = request.url.path

        if path in self.PUBLIC_PATHS:

            return await call_next(request)

        for prefix in self.PUBLIC_PREFIXES:

            if path.startswith(prefix):

                return await call_next(request)

        provided = (
            request.headers.get("x-api-key")
            or request.headers.get(
                "X-Api-Key",
            )
        )

        if provided != secret:

            return JSONResponse(
                {
                    "detail": (
                        "Invalid or missing API key. "
                        "Send header X-Api-Key matching JOB_HUNTER_API_KEY."
                    ),
                },
                status_code=401,
            )

        return await call_next(request)
