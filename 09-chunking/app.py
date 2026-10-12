"""Gradio UI for lesson 09 — chunking + overlap."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import ui
from lib.chunking import chunk_documents
from lib.kb import load_documents


def build() -> gr.Blocks:
    with ui.blocks("09 · Chunking") as demo:
        ui.lesson_shell(
            "09 · Chunking",
            "Документы → чанки с source и overlap (без vector DB)",
            "09-chunking.md",
        )
        size = gr.Slider(200, 1500, value=800, step=50, label="chunk_size")
        overlap = gr.Slider(0, 400, value=150, step=10, label="chunk_overlap")
        run = gr.Button("Нарезать knowledge-base", variant="primary")
        status = gr.Markdown()
        table = gr.Dataframe(
            headers=["#", "type", "source", "chars", "preview"],
            label="Чанки",
            interactive=False,
        )

        def on_run(chunk_size: float, chunk_overlap: float):
            docs = load_documents()
            chunks = chunk_documents(
                docs, chunk_size=int(chunk_size), chunk_overlap=int(chunk_overlap)
            )
            rows = [
                [
                    i + 1,
                    c.doc_type,
                    c.source,
                    len(c.text),
                    c.text[:120].replace("\n", " ") + ("…" if len(c.text) > 120 else ""),
                ]
                for i, c in enumerate(chunks)
            ]
            return (
                f"**{len(docs)}** docs → **{len(chunks)}** chunks · "
                f"size={int(chunk_size)} overlap={int(chunk_overlap)}",
                rows,
            )

        run.click(on_run, inputs=[size, overlap], outputs=[status, table])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8509)
