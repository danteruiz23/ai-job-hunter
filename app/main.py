"""Compatibility entrypoint for uvicorn.

Prefer: uvicorn app.api.main:app --reload

This module re-exports the same app so `uvicorn app.main:app` keeps working.
"""

from app.api.main import app

__all__ = ["app"]
