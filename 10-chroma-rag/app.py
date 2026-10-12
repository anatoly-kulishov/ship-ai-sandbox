"""Gradio UI for lesson 10 — Chroma RAG."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from answer import answer
from lib import ui
from store import embed_model_name, ingest


def build() -> gr.Blocks:
    with ui.blocks("10 · Chroma RAG") as demo:
        ui.lesson_shell(
            "10 · Chroma RAG",
            "Чанки → Ollama embeddings → Chroma → ответ с citations",
            "10-chroma-rag.md",
        )
        ingest_btn = gr.Button("Ingest knowledge-base", variant="secondary")
        ingest_status = gr.Markdown(f"embeddings: `{embed_model_name()}`")
        question = gr.Textbox(label="Вопрос", value="Что такое Draftllm и чем он ограничен?")
        top_k = gr.Slider(2, 8, value=4, step=1, label="top-k")
        run = gr.Button("Спросить", variant="primary")
        status = gr.Markdown()
        reply = gr.Markdown(label="Ответ")
        sources = gr.Code(label="Чанки (JSON)", language="json")

        def on_ingest():
            try:
                n = ingest()
            except Exception as e:
                return f"**Ошибка ingest:** {e}"
            return f"**OK** · {n} векторов · `{embed_model_name()}`"

        def on_ask(q: str, k: float):
            q = (q or "").strip()
            if not q:
                return "Введи вопрос.", "", ""
            try:
                result = answer(q, top_k=int(k))
            except Exception as e:
                return f"**Ошибка:** {e} — сначала Ingest.", "", ""
            hits = result["hits"]
            return (
                f"`{result['provider']}` · `{result['model']}` · hits={len(hits)}",
                result["answer"],
                json.dumps(hits, ensure_ascii=False, indent=2),
            )

        ingest_btn.click(on_ingest, outputs=[ingest_status])
        run.click(on_ask, inputs=[question, top_k], outputs=[status, reply, sources])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8510)
