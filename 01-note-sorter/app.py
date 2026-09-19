"""Streamlit UI for the note sorter."""

from __future__ import annotations

import json

import streamlit as st
from streamlit_mic_recorder import speech_to_text

from categorize import categorize_note, format_result


def render() -> None:
    st.title("01 · Сортировщик заметок")
    st.caption("GigaChat · category + urgent как типизированный ответ")

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
        with st.spinner("GigaChat…"):
            try:
                result = categorize_note(note.strip())
            except Exception as e:
                st.error(str(e))
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
