"""02 · Tool use — LLM calls a real function that writes to SQLite.

Skill: Function Calling / Tool Use.
Model does not return free-form JSON — it invokes save_note(...).
Your code executes the tool → side effect in DB.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.llm import MODEL, get_client  # noqa: E402

DB_PATH = Path(__file__).resolve().parent / "notes.db"

SYSTEM_PROMPT = """
Ты — API-сервис заметок. Не чат-бот.
Единственное действие: вызвать инструмент save_note.
Не отвечай текстом пользователю — только вызов функции.

Правила классификации (как в уроке 01):
- category: WORK | PERSONAL | SHOPPING
- urgent=true только для будущих дел с близким дедлайном
  (срочно, ASAP, сегодня, завтра, вечером).
- urgent=false для прошлого, «на следующей неделе», «когда-нибудь», «если успею», «не срочно».
- бессмысленный ввод → PERSONAL, urgent=false.
""".strip()

SAVE_NOTE_FUNCTION = {
    "name": "save_note",
    "description": "Сохранить классифицированную заметку в базу данных.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Исходный текст заметки"},
            "category": {
                "type": "string",
                "enum": ["WORK", "PERSONAL", "SHOPPING"],
            },
            "urgent": {"type": "boolean"},
        },
        "required": ["text", "category", "urgent"],
    },
}


class Category(str, Enum):
    WORK = "WORK"
    PERSONAL = "PERSONAL"
    SHOPPING = "SHOPPING"


class SaveNoteArgs(BaseModel):
    text: str
    category: Category
    urgent: bool


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                category TEXT NOT NULL,
                urgent INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def save_note(text: str, category: str, urgent: bool) -> dict:
    """Tool implementation — real side effect."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO notes (text, category, urgent) VALUES (?, ?, ?)",
            (text, category, int(urgent)),
        )
        note_id = cur.lastrowid
    return {
        "ok": True,
        "id": note_id,
        "text": text,
        "category": category,
        "urgent": urgent,
    }


def list_notes(limit: int = 20) -> list[dict]:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, text, category, urgent, created_at FROM notes ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {
            "id": r["id"],
            "text": r["text"],
            "category": r["category"],
            "urgent": bool(r["urgent"]),
            "created_at": r["created_at"],
        }
        for r in rows
    ]


TOOLS = {"save_note": lambda **kwargs: save_note(**kwargs)}


def process_note(user_note: str) -> dict:
    """Ask model to call save_note, then execute the tool."""
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_note},
        ],
        # GigaChat: legacy `functions` (not OpenAI `tools`)
        functions=[SAVE_NOTE_FUNCTION],
        function_call={"name": "save_note"},
        temperature=0.0,
    )

    message = response.choices[0].message
    fn = getattr(message, "function_call", None)
    if not fn:
        raise ValueError(f"Model did not call a function. Raw: {message}")

    name = fn.name
    raw_args = fn.arguments
    # GigaChat may return dict; OpenAI-style returns JSON string
    if isinstance(raw_args, str):
        payload = raw_args
    else:
        payload = json.dumps(raw_args, ensure_ascii=False)

    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")

    try:
        args = SaveNoteArgs.model_validate_json(payload)
    except ValidationError as e:
        raise ValueError(f"Invalid tool args: {payload}") from e

    # trust boundary: force original user text into DB, not model rewrite
    return TOOLS[name](
        text=user_note,
        category=args.category.value,
        urgent=args.urgent,
    )


if __name__ == "__main__":
    samples = [
        "Завтра созвон с инвесторами",
        "Надо купить хлеб",
        "Вчера срочно купил молоко",
    ]
    note = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    notes = [note] if note else samples
    for text in notes:
        result = process_note(text)
        print(f"IN:  {text}")
        print(f"OUT: {json.dumps(result, ensure_ascii=False)}")
        print("---")
    print("DB:", DB_PATH)
    print("LAST:", json.dumps(list_notes(5), ensure_ascii=False, indent=2))
