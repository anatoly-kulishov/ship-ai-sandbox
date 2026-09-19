"""Streamlit UI for the note sorter."""

from __future__ import annotations

import json

import streamlit as st

from categorize import categorize_note, format_result

st.set_page_config(page_title="Note Sorter", page_icon="📝", layout="centered")
st.title("Сортировщик заметок")
st.caption("GigaChat · category + urgent как типизированный ответ")

samples = [
    "Блин, забыл, сегодня вечером надо обязательно заехать за кормом для собаки!",
    "Завтра в 10 утра созвон с инвесторами по новому проекту",
    "Надо купить хлеб",
    "Срочно переделать архитектуру базы данных до завтра",
    "В выходные сходить в бассейн",
]

picked = st.selectbox("Пример", ["— своя заметка —", *samples])
default = "" if picked.startswith("—") else picked
note = st.text_area("Текст заметки", value=default, height=120)

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
