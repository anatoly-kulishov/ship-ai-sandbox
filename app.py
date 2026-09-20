"""Lessons Hub — one Streamlit entry for all lessons."""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="ship-ai-sandbox", page_icon="🚢", layout="centered")

st.title("ship-ai-sandbox")
st.caption("Песочница AI Application Engineer")

st.markdown(
    """
Выбери урок в **боковом меню** слева. Конспект (простым языком) - expander **Конспект урока** на странице или файлы в `docs/`.

| Урок | Навык | Конспект |
|---|---|---|
| **01 · Сортировщик** | system prompt → JSON → Pydantic | `docs/01-note-sorter.md` |
| **02 · Tool Use** | function calling → SQLite | `docs/02-tool-use.md` |
| **03 · Ollama** | локальная LLM, тот же API | `docs/03-ollama.md` |
| **04 · Gym Plan** | brief → план с whitelist exerciseId | `docs/04-gym-plan.md` |
| **05 · RAG** | embeddings + cosine по каталогу зала | `docs/05-rag.md` |
| **06 · GGUF** | квантизация Q4/Q5/Q8, модель под RAM | `docs/06-gguf.md` |

CLI (если нужно без UI):
```bash
python 01-note-sorter/categorize.py "текст"
python 02-tool-use/agent.py "текст"
python 03-ollama/check.py "текст"
python 04-gym-plan/check.py "грудь трицепс штанга"
python 05-rag/check.py build
python 05-rag/check.py retrieve "банки"
python 06-gguf/check.py
```
"""
)
