"""Streamlit UI for lesson 05 — gym catalog RAG (embeddings + cosine)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from embeddings import build_embedding_index, load_catalog, load_embedding_index, retrieve
from lib.llm import MODEL, provider_name


def render() -> None:
    st.title("05 · RAG (зал)")
    st.caption("Brief → embeddings → cosine top-k по каталогу упражнений (без Qdrant)")
    st.caption(f"`chat={provider_name()}` · `{MODEL}` · embeddings default `nomic-embed-text`")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "05-rag.md").read_text(encoding="utf-8"))

    catalog = load_catalog()
    index = load_embedding_index()
    st.write(f"Каталог fixture: **{len(catalog)}** · индекс: **{len(index.get('items') or [])}** vec")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Собрать embeddings индекс", type="secondary"):
            with st.spinner("Ollama nomic-embed-text…"):
                payload = build_embedding_index(catalog)
            st.success(f"OK · {len(payload['items'])} × {payload['dims']}")
            st.rerun()
    with col2:
        st.caption("Нужен `ollama pull nomic-embed-text`")

    brief = st.text_input("Brief", value="хочу накачать банки")
    top_k = st.slider("top-k", 5, 40, 15)

    if st.button("Retrieve", type="primary", disabled=not brief.strip()):
        if not (index.get("items") or []):
            st.warning("Индекс пуст — сначала собери embeddings")
        else:
            with st.spinner("embed brief + cosine…"):
                hits = retrieve(brief.strip(), top_k=top_k)
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
            st.dataframe(rows, use_container_width=True)
            st.code(json.dumps(rows[:5], ensure_ascii=False, indent=2), language="json")


if __name__ == "__main__":
    st.set_page_config(page_title="05 RAG", page_icon="🔎", layout="centered")
    render()
