"""Streamlit UI for lesson 04 — gym plan generator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st
from streamlit_mic_recorder import speech_to_text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate import generate_plan, load_catalog
from lib.llm import BASE_URL, MODEL, provider_name


def render() -> None:
    st.title("04 · Gym Plan")
    st.caption("Brief (текст или голос) → план с exerciseId только из каталога (whitelist)")
    provider = provider_name()
    st.caption(f"`LLM_PROVIDER={provider}` · `{MODEL}` · `{BASE_URL}`")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "04-gym-plan.md").read_text(encoding="utf-8"))

    catalog = load_catalog()
    with st.expander(f"Каталог fixture ({len(catalog)} упражнений)"):
        st.dataframe(catalog, use_container_width=True)

    if "gym_brief" not in st.session_state:
        st.session_state.gym_brief = "грудь и трицепс, 45 минут, только штанга и гантели"
    if "gym_last_dictation" not in st.session_state:
        st.session_state.gym_last_dictation = None

    dictated = speech_to_text(
        language="ru-RU",
        start_prompt="🎙 Диктовка",
        stop_prompt="⏹ Стоп",
        just_once=True,
        use_container_width=True,
        key="gym_dictation",
    )
    if dictated and dictated != st.session_state.gym_last_dictation:
        st.session_state.gym_last_dictation = dictated
        existing = st.session_state.gym_brief.strip()
        st.session_state.gym_brief = f"{existing} {dictated}".strip() if existing else dictated

    brief = st.text_area(
        "Brief",
        height=100,
        placeholder="Введи или надиктуй запрос…",
        key="gym_brief",
    )

    if st.button("Сгенерировать план", type="primary", disabled=not brief.strip()):
        with st.spinner(f"{provider}…"):
            try:
                result = generate_plan(brief.strip(), catalog)
            except Exception as e:
                msg = str(e)
                if provider == "ollama" and "Connection" in msg:
                    st.error("Ollama не запущен. `npm run ollama:start` или `npm run provider:gigachat`")
                else:
                    st.error(msg)
            else:
                plan = result["plan"]
                st.success(
                    f"{plan['name']} · {len(plan['exercises'])} упр. · "
                    f"droppedUnknownIds={result['droppedUnknownIds']}"
                )
                st.dataframe(plan["exercises"], use_container_width=True)
                st.code(json.dumps(result, ensure_ascii=False, indent=2), language="json")


if __name__ == "__main__":
    st.set_page_config(page_title="04 Gym Plan", page_icon="🏋", layout="centered")
    render()
