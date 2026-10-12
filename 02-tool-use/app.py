"""Gradio UI for lesson 02 — tool use → SQLite."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent import list_notes, process_note
from lib import ui


def build() -> gr.Blocks:
    with ui.blocks("02 · Tool Use") as demo:
        ui.lesson_shell(
            "02 · Tool Use",
            "Модель вызывает `save_note()` → запись в SQLite",
            "02-tool-use.md",
        )
        note = gr.Textbox(label="Текст заметки", lines=4, placeholder="Введи заметку…")
        run = gr.Button("Сохранить через tool", variant="primary")
        status = gr.Markdown()
        raw = gr.Code(label="Ответ tool", language="json")
        table = gr.Dataframe(label="Последние заметки", interactive=False)

        def refresh_table():
            rows = list_notes(15)
            if not rows:
                return []
            return rows

        def on_run(text: str):
            text = (text or "").strip()
            if not text:
                return "Введи текст.", "", refresh_table()
            try:
                result = process_note(text)
            except Exception as e:
                return f"**Ошибка:** {e}", "", refresh_table()
            msg = (
                f"**Сохранено #{result['id']}:** {result['category']}, "
                f"urgent={result['urgent']}"
            )
            return msg, json.dumps(result, ensure_ascii=False, indent=2), refresh_table()

        demo.load(fn=refresh_table, outputs=table)
        run.click(on_run, inputs=note, outputs=[status, raw, table])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8503)
