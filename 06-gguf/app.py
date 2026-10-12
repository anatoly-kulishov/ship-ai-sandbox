"""Gradio UI for lesson 06 — GGUF / quantization calculator."""

from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import ui
from recommend import report


def build() -> gr.Blocks:
    data = report()
    hw = data["hardware"]
    with ui.blocks("06 · GGUF") as demo:
        ui.lesson_shell(
            "06 · GGUF / quantization",
            "Сколько RAM нужно на Q4/Q5/Q8 и какая модель влезает",
            "06-gguf.md",
        )
        gr.Markdown(
            f"**RAM** {hw['ram_gb']} GB · **usable** {data['usable_gb']} GB · "
            f"**OS reserve** {data['os_reserve_gb']} GB  \n"
            f"{hw['chip']} · unified={hw['unified']} · {hw['os']}"
        )
        gr.Markdown(
            f"**Comfortable:** `{data['recommended']}` · "
            f"**stretch:** `{data['stretch']}` · "
            f"**sandbox JSON:** `{data['sandbox']}`"
        )
        gr.Markdown("### Catalog (Q4 Ollama defaults)")
        gr.Dataframe(value=data["catalog"], interactive=False)
        gr.Markdown("### Same 7B, different quant")
        gr.Dataframe(
            value=[{"quant": q, "ram_gb": gb} for q, gb in data["quant_7b_ram_gb"].items()],
            interactive=False,
        )
        with gr.Accordion("Formula", open=False):
            gr.Markdown(
                """
`RAM ≈ params_B × bytes/param + 1.5 GB runtime`

| Quant | bytes/param | typical Ollama |
|---|---|---|
| Q4_K_M | 0.55 | default `:7b` / `:14b` tags |
| Q5 | 0.70 | чуть лучше Q4 |
| Q8 | 1.05 | почти FP16, ~2× Q4 |
| FP16 | 2.00 | без квантизации |

GGUF = контейнер весов llama.cpp. Ollama его и крутит.
"""
            )
        gr.Markdown("### Installed in Ollama")
        if data["installed"]:
            gr.Dataframe(value=data["installed"], interactive=False)
        else:
            gr.Markdown("Ollama не отвечает на `:11434`. Урок **не** требует pull.")
        gr.Markdown("Этот урок ничего не качает. `ollama pull` - отдельное решение.")
    return demo


if __name__ == "__main__":
    ui.launch(build(), port=8507)
