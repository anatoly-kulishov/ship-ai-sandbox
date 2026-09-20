"""Backward-compatible re-export. Prefer `from lib.llm import ...`."""

from lib.llm import (  # noqa: F401
    BASE_URL,
    MODEL,
    fetch_access_token,
    get_client,
    provider_name,
)
