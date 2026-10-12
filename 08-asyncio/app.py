"""Gradio guide page for lesson 08 — asyncio gateway (server is separate)."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import ui


def build() -> gr.Blocks:
    with ui.blocks("08 · Asyncio") as demo:
        ui.lesson_shell(
            "08 · Asyncio + AsyncOpenAI",
            "Почему LLM-gateway должен быть async",
            "08-asyncio.md",
        )
        gr.Markdown(
            """
Отдельный FastAPI на порту **8601** (урок 07 - на 8600).

### Запуск
```bash
npm run 08
```
Swagger: http://localhost:8601/docs

### Что попробовать
- `POST /demo/sleep` - 3 параллельных sleep: wall ≈ 0.4с, не 1.2с
- `POST /classify` - async классификация
- `POST /demo/classify` - batch через `asyncio.gather`
- `POST /plan` - sync `generate_plan` через `asyncio.to_thread`

### Самопроверка
```bash
npm run check:08
```
"""
        )
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8509)
