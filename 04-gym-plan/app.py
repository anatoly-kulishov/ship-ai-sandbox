"""Gradio UI for lesson 04 — gym plan generator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate import generate_plan, load_catalog
from lib import ui
from lib.llm import BASE_URL, MODEL, provider_name


def build() -> gr.Blocks:
    catalog = load_catalog()
    with ui.blocks("04 · Gym Plan") as demo:
        ui.lesson_shell(
            "04 · Gym Plan",
            f"Brief → план с whitelist exerciseId · `{provider_name()}` · `{MODEL}` · `{BASE_URL}`",
            "04-gym-plan.md",
        )
        with gr.Accordion(f"Каталог fixture ({len(catalog)} упражнений)", open=False):
            gr.Dataframe(value=catalog, interactive=False, wrap=True)

        brief = gr.Textbox(
            label="Brief",
            lines=3,
            value="грудь и трицепс, 45 минут, только штанга и гантели",
            placeholder="Зоны, оборудование, время…",
        )
        run = gr.Button("Сгенерировать план", variant="primary")
        status = gr.Markdown()
        table = gr.Dataframe(label="Упражнения", interactive=False)
        raw = gr.Code(label="JSON ответа", language="json")

        def on_run(text: str):
            text = (text or "").strip()
            if not text:
                return "Введи brief.", [], ""
            try:
                result = generate_plan(text, catalog)
            except Exception as e:
                msg = str(e)
                if provider_name() == "ollama" and "Connection" in msg:
                    return (
                        "Ollama не запущен. `npm run ollama:start` или `npm run provider:gigachat`",
                        [],
                        "",
                    )
                return f"**Ошибка:** {msg}", [], ""
            plan = result["plan"]
            msg = (
                f"**{plan['name']}** · {len(plan['exercises'])} упр. · "
                f"droppedUnknownIds={result['droppedUnknownIds']}"
            )
            return (
                msg,
                plan["exercises"],
                json.dumps(result, ensure_ascii=False, indent=2),
            )

        run.click(on_run, inputs=brief, outputs=[status, table, raw])
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8505)
