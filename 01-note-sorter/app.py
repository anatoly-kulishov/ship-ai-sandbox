"""Gradio UI for lesson 01 — note sorter."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from categorize import categorize_note, format_result
from lib import ui
from lib.llm import BASE_URL, MODEL, provider_name


def build() -> gr.Blocks:
    with ui.blocks("01 · Сортировщик") as demo:
        ui.lesson_shell(
            "01 · Сортировщик заметок",
            f"`{provider_name()}` · `{MODEL}` · `{BASE_URL}`",
            "01-note-sorter.md",
        )
        note = gr.Textbox(
            label="Текст заметки",
            lines=5,
            placeholder="Например: завтра созвон с инвесторами / купить хлеб сегодня",
        )
        run = gr.Button("Классифицировать", variant="primary")
        status = gr.Markdown()
        category = gr.Textbox(label="Категория", interactive=False)
        urgent = gr.Textbox(label="Срочность", interactive=False)
        raw = gr.Code(label="JSON", language="json")

        def on_run(text: str):
            text = (text or "").strip()
            if not text:
                return "Введи текст заметки.", "", "", ""
            try:
                result = categorize_note(text)
            except Exception as e:
                msg = str(e)
                if provider_name() == "ollama" and (
                    "Connection" in msg or "11434" in msg or "refused" in msg.lower()
                ):
                    return (
                        "Ollama не запущен. `npm run ollama:start` или `npm run provider:gigachat`",
                        "",
                        "",
                        "",
                    )
                return f"**Ошибка:** {msg}", "", "", ""
            payload = json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2)
            return (
                f"**OK.** {format_result(result)}",
                result.category.value,
                str(result.urgent),
                payload,
            )

        run.click(on_run, inputs=note, outputs=[status, category, urgent, raw])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8502)
