"""01 · Note sorter — LLM as a typed function.

Skill: system prompt + JSON schema + Pydantic validation,
so the model returns data your frontend/DB can trust.

GigaChat Freemium: LLM_API_KEY = Authorization key from Studio
(exchanged for a 30-min access token via OAuth).
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from enum import Enum
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

AUTH_KEY = (os.getenv("LLM_API_KEY") or "").removeprefix("sk-")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.giga.chat/v1")
MODEL = os.getenv("LLM_MODEL", "GigaChat-2")
OAUTH_URL = os.getenv(
    "LLM_OAUTH_URL",
    "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
)
SCOPE = os.getenv("LLM_SCOPE", "GIGACHAT_API_PERS")
# ponytail: Минцифры CA often missing on Mac; set LLM_SSL_VERIFY=true after installing certs
SSL_VERIFY = os.getenv("LLM_SSL_VERIFY", "false").lower() in {"1", "true", "yes"}

if not AUTH_KEY:
    raise SystemExit(
        "Missing LLM_API_KEY — paste GigaChat Authorization key from Studio "
        "(developers.sber.ru → GigaChat API → Получить ключ)."
    )


def fetch_access_token() -> str:
    """Exchange Studio Authorization key for a short-lived Bearer token."""
    response = requests.post(
        OAUTH_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {AUTH_KEY}",
        },
        data={"scope": SCOPE},
        timeout=30,
        verify=SSL_VERIFY,
    )
    if not response.ok:
        raise SystemExit(
            f"GigaChat OAuth failed ({response.status_code}): {response.text[:500]}"
        )
    token = response.json().get("access_token")
    if not token:
        raise SystemExit(f"GigaChat OAuth: no access_token in {response.text[:500]}")
    return token


client = OpenAI(api_key=fetch_access_token(), base_url=BASE_URL)


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
    # GigaChat may ignore / reject response_format; prompt + Pydantic is the real contract
    try:
        response = client.chat.completions.create(
            **kwargs,
            response_format={"type": "json_object"},
        )
    except Exception:
        response = client.chat.completions.create(**kwargs)

    raw = response.choices[0].message.content or "{}"
    # strip accidental markdown fences
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
