"""Ollama embeddings helper shared by RAG lessons."""

from __future__ import annotations

import os

import requests

MODEL = (os.getenv("EMBEDDINGS_MODEL") or "nomic-embed-text").strip()
OLLAMA_BASE = (os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434/v1").rstrip("/").removesuffix(
    "/v1"
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    out: list[list[float]] = []
    for prompt in texts:
        r = requests.post(
            f"{OLLAMA_BASE}/api/embeddings",
            json={"model": MODEL, "prompt": prompt},
            timeout=60,
        )
        r.raise_for_status()
        emb = r.json().get("embedding")
        if not isinstance(emb, list):
            raise RuntimeError("ollama embeddings: missing embedding")
        out.append(emb)
    return out
