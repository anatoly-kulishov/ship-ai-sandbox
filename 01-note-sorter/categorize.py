"""01 · Note sorter — LLM as a typed function.

Works with any OpenAI-compatible provider via lib.llm
(GigaChat OAuth or Ollama at localhost:11434).
"""

from __future__ import annotations

import json
import sys
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.llm import MODEL, get_client  # noqa: E402

_client = None


def client():
    global _client
    if _client is None:
        _client = get_client()
    return _client


class Category(str, Enum):
    WORK = "WORK"
    PERSONAL = "PERSONAL"
    SHOPPING = "SHOPPING"


class NoteClassification(BaseModel):
    category: Category
    urgent: bool


SYSTEM_PROMPT = """
Ты — API-сервис классификации заметок. Не чат-бот.

Правила:
1. Верни ТОЛЬКО валидный JSON без markdown, пояснений и преамбул.
2. Схема ответа строго:
   {"category": "<CATEGORY>", "urgent": <true|false>}
3. category — ровно одно из: WORK | PERSONAL | SHOPPING
   - WORK: работа, проекты, встречи, код, коллеги, инвесторы
   - PERSONAL: быт, здоровье, семья, хобби, личные дела (не покупки)
   - SHOPPING: покупки, еда, товары, магазины, корм, продукты
4. urgent = true только если действие ещё предстоит И есть явный близкий дедлайн/срочность:
   «срочно», «ASAP», «сегодня», «завтра», «до завтра», «вечером», «в 10 утра».
   urgent = false, если:
   - нет маркеров срочности;
   - дедлайн далёкий или размытый: «на следующей неделе», «когда-нибудь», «потом», «если успею», «может»;
   - событие уже в прошлом («вчера», «уже купил», «сделал»), даже если есть слово «срочно»;
   - есть отрицание срочности («не срочно»).
5. Если текст бессмысленный/пустой/эмодзи/цифры без задачи — всё равно верни валидный JSON:
   {"category": "PERSONAL", "urgent": false}
6. Если категория неоднозначна — выбери наиболее вероятную. Никогда не выдумывай другие поля или значения.
""".strip()


def categorize_note(user_note: str) -> NoteClassification:
    kwargs: dict = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_note},
        ],
        "temperature": 0.0,
    }
    try:
        response = client().chat.completions.create(
            **kwargs,
            response_format={"type": "json_object"},
        )
    except Exception:
        response = client().chat.completions.create(**kwargs)

    raw = response.choices[0].message.content or "{}"
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:].strip()

    try:
        return NoteClassification.model_validate_json(raw)
    except ValidationError as e:
        raise ValueError(f"Model returned invalid payload: {raw}") from e


def format_result(result: NoteClassification) -> str:
    return f"Категория: {result.category.value}, Срочность: {result.urgent}"


if __name__ == "__main__":
    samples = [
        "Блин, забыл, сегодня вечером надо обязательно заехать за кормом для собаки!",
        "Завтра в 10 утра созвон с инвесторами по новому проекту",
        "Надо купить хлеб",
        "Срочно переделать архитектуру базы данных до завтра",
        "В выходные сходить в бассейн",
    ]

    note = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    notes = [note] if note else samples

    for text in notes:
        result = categorize_note(text)
        print(f"IN:  {text}")
        print(f"OUT: {format_result(result)}")
        print(f"JSON: {json.dumps(result.model_dump(mode='json'), ensure_ascii=False)}")
        print("---")
