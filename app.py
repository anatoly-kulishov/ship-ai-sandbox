"""Lessons Hub — one Streamlit entry for all lessons."""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="ship-ai-sandbox", page_icon="🚢", layout="centered")

st.title("ship-ai-sandbox")
st.caption("Песочница AI Application Engineer")

st.markdown(
    """
Выбери урок в **боковом меню** слева.

| Урок | Навык |
|---|---|
| **01 · Сортировщик** | system prompt → JSON → Pydantic |
| **02 · Tool Use** | function calling → SQLite |

CLI (если нужно без UI):
```bash
python 01-note-sorter/categorize.py "текст"
python 02-tool-use/agent.py "текст"
```
"""
)
