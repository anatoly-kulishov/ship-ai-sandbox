"""Gradio UI for lesson 12 — Postgres event log."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import init_schema, list_events, ping
from lib import ui
from lib.llm import MODEL, provider_name


def build() -> gr.Blocks:
    with ui.blocks("12 · Postgres") as demo:
        ui.lesson_shell(
            "12 · PostgreSQL",
            "LLM-вызов → строка в Postgres (events). Не только SQLite.",
            "12-postgres.md",
        )
        meta = gr.Markdown()
        text = gr.Textbox(label="Заметка", value="сегодня купить хлеб")
        run = gr.Button("Classify + записать в Postgres", variant="primary")
        refresh = gr.Button("Обновить ленту", variant="secondary")
        status = gr.Markdown()
        table = gr.Dataframe(
            headers=["id", "kind", "brief", "payload", "created_at"],
            label="events (последние)",
            interactive=False,
        )

        def _meta() -> str:
            try:
                init_schema()
                info = ping()
                return (
                    f"`chat={provider_name()}` · `{MODEL}` · "
                    f"db=`{info['db']}` · `{info['version']}`"
                )
            except Exception as e:  # noqa: BLE001
                return f"**Postgres недоступен:** {e}"

        def _rows(limit: int = 15):
            try:
                evs = list_events(limit=limit)
            except Exception:
                return []
            return [
                [
                    e["id"],
                    e["kind"],
                    e["brief"][:80],
                    json.dumps(e["payload"], ensure_ascii=False)[:120],
                    e["created_at"],
                ]
                for e in evs
            ]

        def on_run(note: str):
            note = (note or "").strip()
            if not note:
                return "Введи текст.", _rows(), _meta()
            try:
                init_schema()
                # lazy import — needs LLM only on click
                from server import NoteIn, classify

                out = classify(NoteIn(text=note))
            except Exception as e:  # noqa: BLE001
                return f"**Ошибка:** {e}", _rows(), _meta()
            return (
                f"**OK** event #{out['event']['id']} · {out['result']}",
                _rows(),
                _meta(),
            )

        def on_refresh():
            return _rows(), _meta()

        meta.value = _meta()
        run.click(on_run, inputs=[text], outputs=[status, table, meta])
        refresh.click(on_refresh, outputs=[table, meta])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8512)
