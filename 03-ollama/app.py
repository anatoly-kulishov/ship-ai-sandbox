"""Gradio UI for lesson 03 — local Ollama."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "01-note-sorter"))

from categorize import categorize_note, format_result
from lib import ui
from lib.llm import BASE_URL, MODEL, ping, provider_name


def build() -> gr.Blocks:
    with ui.blocks("03 · Ollama") as demo:
        ui.lesson_shell(
            "03 · Ollama (local LLM)",
            "Тот же сортировщик, но модель на твоём компьютере",
            "03-ollama.md",
        )
        gr.Markdown(
            f"**LLM_PROVIDER:** `{provider_name()}`  \n"
            f"**URL:** `{BASE_URL}`  \n"
            f"**Модель:** `{MODEL}`  \n\n"
            "Переключение: `npm run provider:ollama` / `provider:gigachat`"
        )
        ping_out = gr.Markdown()
        note = gr.Textbox(label="Текст заметки", lines=4)
        run = gr.Button("Классифицировать локально", variant="primary")
        status = gr.Markdown()
        raw = gr.Code(label="JSON", language="json")

        def do_ping():
            try:
                info = ping()
                return f"**OK** · models: `{info.get('models', info.get('model'))}`"
            except Exception as e:
                return (
                    "Ollama не отвечает.\n\n"
                    "`npm run ollama:start` · в `.env`: `LLM_PROVIDER=ollama`\n\n"
                    f"`{e}`"
                )

        def on_run(text: str):
            text = (text or "").strip()
            if not text:
                return "Введи текст.", ""
            try:
                result = categorize_note(text)
            except Exception as e:
                return f"**Ошибка:** {e}", ""
            return (
                f"**OK.** {format_result(result)}",
                json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2),
            )

        demo.load(do_ping, outputs=ping_out)
        run.click(on_run, inputs=note, outputs=[status, raw])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8504)
