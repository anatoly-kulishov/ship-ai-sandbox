"""Streamlit UI for lesson 03 — local Ollama."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "01-note-sorter"))

from categorize import categorize_note, format_result
from lib.llm import BASE_URL, MODEL, ping, provider_name


def render() -> None:
    st.title("03 · Ollama (local LLM)")
    st.caption("Тот же сортировщик, но модель на твоём компьютере")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "03-ollama.md").read_text(encoding="utf-8"))

    st.markdown(
        f"""
**LLM_PROVIDER:** `{provider_name()}`  
**URL:** `{BASE_URL}`  
**Модель:** `{MODEL}`

Переключение в `.env`: `LLM_PROVIDER=ollama` или `gigachat`
"""
    )

    try:
        info = ping()
        st.success(f"OK · models: {info.get('models', info.get('model'))}")
    except Exception as e:
        st.error(
            "Ollama не отвечает. В терминале:\n\n"
            "```bash\n"
            "ollama serve\n"
            "ollama pull qwen2.5:3b\n"
            "```\n\n"
            "В `.env`:\n"
            "```\n"
            "LLM_PROVIDER=ollama\n"
            "```\n"
            "и запусти `./scripts/start-ollama.sh`\n\n"
            f"`{e}`"
        )
        return

    note = st.text_area("Текст заметки", height=120, key="ollama_note")
    if st.button("Классифицировать локально", type="primary", disabled=not note.strip()):
        with st.spinner("Local LLM…"):
            try:
                result = categorize_note(note.strip())
            except Exception as e:
                st.error(str(e))
            else:
                st.success(format_result(result))
                st.code(
                    json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2),
                    language="json",
                )


if __name__ == "__main__":
    st.set_page_config(page_title="03 Ollama", page_icon="🦙", layout="centered")
    render()
