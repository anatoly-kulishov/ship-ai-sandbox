"""Hub UI for lesson 07 — FastAPI gateway."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


def render() -> None:
    st.set_page_config(page_title="07 · FastAPI gateway", page_icon="🚀")
    st.title("07 · FastAPI gateway")
    st.caption("HTTP API над генератором плана и RAG retrieve")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "07-fastapi.md").read_text(encoding="utf-8"))

    st.markdown(
        """
        Этот урок не запускается внутри Streamlit — он **самостоятельный FastAPI-сервер**.

        ### Запуск
        ```bash
        npm run 07
        ```
        Сервер поднимется на `http://localhost:8600`.

        ### Swagger UI
        Открой `http://localhost:8600/docs` — там можно вызвать endpoints вручную:
        - `GET /health` — проверка провайдера
        - `POST /plan` — brief → план тренировки
        - `POST /retrieve` — semantic search по каталогу

        ### Самопроверка
        ```bash
        npm run check:07
        ```
        """
    )


if __name__ == "__main__":
    render()
