"""RAG answer: retrieve chunks → LLM with «не знаю» rule."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.llm import MODEL, get_client, provider_name
from store import retrieve

SYSTEM = """Ты knowledge-worker Fitllm. Отвечай только по CONTEXT.
Если ответа нет в CONTEXT — скажи «не знаю по базе Fitllm».
Кратко. Укажи source, если уместно. Язык: русский."""


def answer(question: str, *, top_k: int = 4) -> dict:
    hits = retrieve(question, top_k=top_k)
    context = "\n\n".join(
        f"[{h['source']}]\n{h['text']}" for h in hits
    )
    client = get_client()
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}",
            },
        ],
    )
    text = (resp.choices[0].message.content or "").strip()
    return {
        "answer": text,
        "hits": hits,
        "provider": provider_name(),
        "model": MODEL,
    }
