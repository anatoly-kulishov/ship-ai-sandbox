"""Gradio UI for lesson 05 — gym catalog RAG."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from embeddings import build_embedding_index, load_catalog, load_embedding_index, retrieve
from lib import ui
from lib.llm import MODEL, provider_name


def _index_caption() -> str:
    catalog = load_catalog()
    index = load_embedding_index()
    n_vec = len(index.get("items") or [])
    return (
        f"`chat={provider_name()}` · `{MODEL}` · embeddings `nomic-embed-text`  \n"
        f"Каталог: **{len(catalog)}** · индекс: **{n_vec}** vec"
    )


def build() -> gr.Blocks:
    with ui.blocks("05 · RAG") as demo:
        ui.lesson_shell(
            "05 · RAG (зал)",
            "Brief → embeddings → cosine top-k (без Qdrant)",
            "05-rag.md",
        )
        meta = gr.Markdown(_index_caption())
        build_btn = gr.Button("Собрать embeddings индекс", variant="secondary")
        build_status = gr.Markdown("Нужен `ollama pull nomic-embed-text`")
        brief = gr.Textbox(label="Brief", value="хочу накачать банки")
        top_k = gr.Slider(5, 40, value=15, step=1, label="top-k")
        run = gr.Button("Retrieve", variant="primary")
        status = gr.Markdown()
        table = gr.Dataframe(label="Top-k", interactive=False)
        raw = gr.Code(label="Первые 5 (JSON)", language="json")

        def on_build():
            try:
                payload = build_embedding_index(load_catalog())
            except Exception as e:
                return f"**Ошибка сборки:** {e}", _index_caption()
            return (
                f"**OK** · {len(payload['items'])} × dims={payload['dims']}",
                _index_caption(),
            )

        def on_retrieve(text: str, k: float):
            text = (text or "").strip()
            if not text:
                return "Введи brief.", [], ""
            index = load_embedding_index()
            if not (index.get("items") or []):
                return "Индекс пуст — сначала собери embeddings.", [], ""
            try:
                hits = retrieve(text, top_k=int(k))
            except Exception as e:
                return f"**Ошибка:** {e}", [], ""
            rows = [
                {
                    "id": ex["id"],
                    "name": ex.get("name_ru") or ex.get("name"),
                    "body_part": ex["body_part"],
                    "target": ex["target"],
                    "equipment": ex["equipment"],
                }
                for ex in hits
            ]
            return (
                f"**{len(rows)}** упражнений",
                rows,
                json.dumps(rows[:5], ensure_ascii=False, indent=2),
            )

        build_btn.click(on_build, outputs=[build_status, meta])
        run.click(on_retrieve, inputs=[brief, top_k], outputs=[status, table, raw])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8506)
