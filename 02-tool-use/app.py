"""Streamlit UI for tool-use note saver."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import list_notes, process_note


def render() -> None:
    st.title("02 · Tool Use")
    st.caption("Модель вызывает save_note() → запись в SQLite")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "02-tool-use.md").read_text(encoding="utf-8"))

    note = st.text_area(
        "Текст заметки",
        height=120,
        placeholder="Введи заметку…",
        key="tool_note",
    )

    if st.button("Сохранить через tool", type="primary", disabled=not note.strip()):
        with st.spinner("GigaChat → tool call…"):
            try:
                result = process_note(note.strip())
            except Exception as e:
                st.error(str(e))
            else:
                st.success(
                    f"Сохранено #{result['id']}: {result['category']}, "
                    f"urgent={result['urgent']}"
                )
                st.code(json.dumps(result, ensure_ascii=False, indent=2), language="json")

    st.subheader("Последние заметки")
    rows = list_notes(15)
    if not rows:
        st.info("База пуста")
    else:
        st.dataframe(rows, use_container_width=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Tool Use · Notes", page_icon="🛠", layout="centered")
    render()
