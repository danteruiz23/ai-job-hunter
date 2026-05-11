import os

from fastapi import HTTPException
from fastapi import UploadFile


MAX_UPLOAD_BYTES = int(
    os.getenv(
        "MAX_UPLOAD_BYTES",
        str(15 * 1024 * 1024),
    )
)


def require_openai_key():
    if not os.getenv("OPENAI_API_KEY", "").strip():
        raise HTTPException(
            status_code=503,
            detail=(
                "OPENAI_API_KEY is not configured. "
                "Add it to your .env file in the project root."
            ),
        )


async def read_upload_with_limit(
    file: UploadFile,
) -> bytes:

    body = await file.read()

    if len(body) > MAX_UPLOAD_BYTES:

        mb = MAX_UPLOAD_BYTES // (1024 * 1024)

        raise HTTPException(
            status_code=413,
            detail=(
                f"File too large (max {mb} MB). "
                "Reduce file size or raise MAX_UPLOAD_BYTES in .env."
            ),
        )

    return body
