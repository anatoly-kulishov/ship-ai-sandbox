"""Async note classification — same contract as lesson 01, AsyncOpenAI under the hood."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "01-note-sorter"))

from categorize import SYSTEM_PROMPT, NoteClassification  # noqa: E402
from lib.llm import MODEL, get_async_client  # noqa: E402


def _strip_fences(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    return text


async def categorize_note_async(user_note: str) -> NoteClassification:
    client = await get_async_client()
    kwargs: dict = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_note},
        ],
        "temperature": 0.0,
    }
    try:
        response = await client.chat.completions.create(
            **kwargs,
            response_format={"type": "json_object"},
        )
    except Exception:
        response = await client.chat.completions.create(**kwargs)

    raw = _strip_fences(response.choices[0].message.content or "{}")
    try:
        return NoteClassification.model_validate_json(raw)
    except ValidationError as e:
        raise ValueError(f"Model returned invalid payload: {raw}") from e
