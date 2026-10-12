"""Lessons Hub — Gradio multipage app for studying."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from lib import ui  # noqa: E402

LESSONS: list[tuple[str, str, str]] = [
    ("01 · Сортировщик", "/01", "01-note-sorter"),
    ("02 · Tool Use", "/02", "02-tool-use"),
    ("03 · Ollama", "/03", "03-ollama"),
    ("04 · Gym Plan", "/04", "04-gym-plan"),
    ("05 · RAG", "/05", "05-rag"),
    ("06 · GGUF", "/06", "06-gguf"),
    ("07 · FastAPI", "/07", "07-fastapi"),
    ("08 · Asyncio", "/08", "08-asyncio"),
    ("09 · Chunking", "/09", "09-chunking"),
    ("10 · Chroma", "/10", "10-chroma-rag"),
    ("11 · LangChain", "/11", "11-langchain-rag"),
    ("12 · Postgres", "/12", "12-postgres"),
]


def _load_build(folder: str):
    path = ROOT / folder / "app.py"
    spec = importlib.util.spec_from_file_location(f"lesson_{folder}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.build


def build_hub() -> gr.Blocks:
    with ui.blocks("ship-ai-sandbox") as demo:
        gr.Markdown(
            """
# ship-ai-sandbox
Песочница **AI Application Engineer**: модель в продукте, не чат.

Выбери урок в **навигации сверху**. На каждой странице - accordion **Конспект урока**.

Теория (Ed Donner → наши заметки): [`docs/theory/`](docs/theory/README.md) · карта: [`docs/sources/ed-donner.md`](docs/sources/ed-donner.md)

| Урок | Навык | Конспект |
|---|---|---|
| 01 | system prompt → JSON → Pydantic | `docs/01-note-sorter.md` |
| 02 | function calling → SQLite | `docs/02-tool-use.md` |
| 03 | локальная LLM (Ollama) | `docs/03-ollama.md` |
| 04 | brief → план, whitelist id | `docs/04-gym-plan.md` |
| 05 | embeddings + cosine | `docs/05-rag.md` |
| 06 | GGUF / Q4-Q8 под RAM | `docs/06-gguf.md` |
| 07 | FastAPI gateway (:8600) | `docs/07-fastapi.md` |
| 08 | AsyncOpenAI (:8601) | `docs/08-asyncio.md` |
| 09 | chunking + overlap | `docs/09-chunking.md` |
| 10 | Chroma docs-RAG | `docs/10-chroma-rag.md` |
| 11 | LangChain RAG | `docs/11-langchain-rag.md` |
| 12 | Postgres event log | `docs/12-postgres.md` |

```bash
npm run provider:ollama   # или gigachat
npm run postgres:up       # урок 12
npm run check:12
```
"""
        )

    for title, path, folder in LESSONS:
        page = _load_build(folder)()
        with demo.route(title, path):
            page.render()

    return demo


if __name__ == "__main__":
    ui.launch(build_hub(), port=8501)
