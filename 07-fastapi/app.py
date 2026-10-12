"""Gradio guide page for lesson 07 — FastAPI gateway (server is separate)."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import ui


def build() -> gr.Blocks:
    with ui.blocks("07 · FastAPI") as demo:
        ui.lesson_shell(
            "07 · FastAPI gateway",
            "HTTP API над генератором плана и RAG retrieve",
            "07-fastapi.md",
        )
        gr.Markdown(
            """
Этот урок - **отдельный FastAPI-сервер**, не виджет внутри Gradio.

### Запуск
```bash
npm run 07
```
Сервер: http://localhost:8600 · Swagger: http://localhost:8600/docs

### Endpoints
- `GET /health` - провайдер
- `POST /plan` - brief → план
- `POST /retrieve` - semantic search

### Самопроверка
```bash
npm run check:07
```
"""
        )
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8508)
