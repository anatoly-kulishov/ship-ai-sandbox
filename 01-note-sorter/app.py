"""Streamlit UI for the note sorter."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st
from streamlit_mic_recorder import speech_to_text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from categorize import categorize_note, format_result
from lib.llm import BASE_URL, MODEL, provider_name


def render() -> None:
    st.title("01 · Сортировщик заметок")
    provider = provider_name()
    st.caption(f"{provider} · {MODEL} · category + urgent")
    st.caption(f"`LLM_PROVIDER={provider}` · `{BASE_URL}`")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "01-note-sorter.md").read_text(encoding="utf-8"))

    if "note" not in st.session_state:
        st.session_state.note = ""
    if "last_dictation" not in st.session_state:
        st.session_state.last_dictation = None

    dictated = speech_to_text(
        language="ru-RU",
        start_prompt="🎙 Диктовка",
        stop_prompt="⏹ Стоп",
        just_once=True,
        use_container_width=True,
        key="note_dictation",
    )
    if dictated and dictated != st.session_state.last_dictation:
        st.session_state.last_dictation = dictated
        existing = st.session_state.note.strip()
        st.session_state.note = f"{existing} {dictated}".strip() if existing else dictated

    note = st.text_area(
        "Текст заметки",
        height=140,
        placeholder="Введи или надиктуй заметку…",
        key="note",
    )

    if st.button("Классифицировать", type="primary", disabled=not note.strip()):
        with st.spinner(f"{provider}…"):
            try:
                result = categorize_note(note.strip())
            except Exception as e:
                msg = str(e)
                if provider == "ollama" and (
                    "Connection" in msg or "11434" in msg or "refused" in msg.lower()
                ):
                    st.error(
                        "Ollama не запущен.\n\n"
                        "`npm run ollama:start`\n"
                        "или переключись: `npm run provider:gigachat`"
                    )
                else:
                    st.error(msg)
            else:
                st.success(format_result(result))
                c1, c2 = st.columns(2)
                c1.metric("Категория", result.category.value)
                c2.metric("Срочность", "True" if result.urgent else "False")
                st.code(
                    json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2),
                    language="json",
                )


if __name__ == "__main__":
    st.set_page_config(page_title="Note Sorter", page_icon="📝", layout="centered")
    render()
