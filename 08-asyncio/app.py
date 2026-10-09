"""Hub UI for lesson 08 — asyncio + AsyncOpenAI."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


def render() -> None:
    st.set_page_config(page_title="08 · Asyncio", page_icon=":material/bolt:")
    st.title("08 · Asyncio + AsyncOpenAI")
    st.caption("Почему LLM-gateway должен быть async, и как это выглядит в коде")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "08-asyncio.md").read_text(encoding="utf-8"))

    st.markdown(
        """
        Отдельный FastAPI на порту **8601** (07 живёт на 8600).

        ### Запуск
        ```bash
        npm run 08
        ```
        Swagger: http://localhost:8601/docs

        ### Что попробовать
        - `POST /demo/sleep` — 3 параллельных sleep: wall ≈ 0.4с, не 1.2с
        - `POST /classify` — async классификация (урок 01 на AsyncOpenAI)
        - `POST /demo/classify` — несколько заметок сразу через `asyncio.gather`
        - `POST /plan` — старый sync `generate_plan` через `asyncio.to_thread`

        ### Самопроверка
        ```bash
        npm run check:08
        ```
        """
    )


if __name__ == "__main__":
    render()
