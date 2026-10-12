"""Shared Gradio helpers for the lessons hub."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
THEME = gr.themes.Soft(
    primary_hue="slate",
    secondary_hue="blue",
    neutral_hue="slate",
)
CSS = """
.lesson-cap { opacity: 0.8; font-size: 0.95rem; }
footer { display: none !important; }
"""


def read_doc(name: str) -> str:
    path = ROOT / "docs" / name
    return path.read_text(encoding="utf-8")


def blocks(title: str) -> gr.Blocks:
    # Gradio 5: theme/css on Blocks. (Gradio 6 may move them to launch.)
    return gr.Blocks(title=title, theme=THEME, css=CSS)


def lesson_shell(title: str, caption: str, doc_file: str) -> None:
    """Title + caption + collapsed conspect. Call inside an open Blocks context."""
    gr.Markdown(f"# {title}\n<p class='lesson-cap'>{caption}</p>")
    with gr.Accordion("Конспект урока (простым языком)", open=False):
        gr.Markdown(read_doc(doc_file))


def launch(demo: gr.Blocks, *, port: int, share: bool = False) -> None:
    demo.queue(default_concurrency_limit=4)
    demo.launch(
        server_name="127.0.0.1",
        server_port=port,
        share=share,
        show_error=True,
    )
