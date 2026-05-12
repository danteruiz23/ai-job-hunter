"""Lazy OpenAI client so API imports succeed before env vars are read at call time."""

from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    """Reads OPENAI_API_KEY from the environment when first used."""
    return OpenAI()
