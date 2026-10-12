"""Gradio UI for lesson 11 — LangChain RAG."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import ui
from pipeline import ask, ingest


def build() -> gr.Blocks:
    with ui.blocks("11 · LangChain RAG") as demo:
        ui.lesson_shell(
            "11 · LangChain RAG",
            "Тот же Fitllm RAG: LC splitter + Chroma + LC prompt chain",
            "11-langchain-rag.md",
        )
        ingest_btn = gr.Button("Ingest (LangChain)", variant="secondary")
        ingest_status = gr.Markdown("Отдельная папка `vector_db_lc/`")
        question = gr.Textbox(label="Вопрос", value="Зачем нужен whitelist id?")
        top_k = gr.Slider(2, 8, value=4, step=1, label="top-k")
        run = gr.Button("Спросить", variant="primary")
        status = gr.Markdown()
        reply = gr.Markdown()
        sources = gr.Code(language="json")

        def on_ingest():
            try:
                n = ingest()
            except Exception as e:
                return f"**Ошибка:** {e}"
            return f"**OK** · {n} чанков в Chroma (LC)"

        def on_ask(q: str, k: float):
            q = (q or "").strip()
            if not q:
                return "Введи вопрос.", "", ""
            try:
                result = ask(q, top_k=int(k))
            except Exception as e:
                return f"**Ошибка:** {e} — сначала Ingest.", "", ""
            return (
                f"`{result['provider']}` · `{result['model']}` · hits={len(result['hits'])}",
                result["answer"],
                json.dumps(result["hits"], ensure_ascii=False, indent=2),
            )

        ingest_btn.click(on_ingest, outputs=[ingest_status])
        run.click(on_ask, inputs=[question, top_k], outputs=[status, reply, sources])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8511)
