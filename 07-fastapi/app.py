"""Hub UI for lesson 07 — FastAPI gateway."""

from __future__ import annotations

import streamlit as st


def render() -> None:
    st.set_page_config(page_title="07 · FastAPI gateway", page_icon="🚀")
    st.title("07 · FastAPI gateway")
    st.caption("HTTP API над генератором плана и RAG retrieve")

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

        ### Конспект
        Подробности в `docs/07-fastapi.md`.
        """
    )


if __name__ == "__main__":
    render()
