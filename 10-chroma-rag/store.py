"""Chroma ingest + retrieve for Fitllm docs (Ollama embeddings)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.chunking import chunk_documents
from lib.kb import load_documents
from lib.ollama_embed import MODEL, embed_texts

DB_DIR = Path(__file__).resolve().parent / "vector_db"
COLLECTION = "fitllm"


class OllamaEF(EmbeddingFunction[Documents]):
    def __call__(self, input: Documents) -> Embeddings:
        return embed_texts(list(input))


def ingest(*, chunk_size: int = 800, chunk_overlap: int = 150, reset: bool = True) -> int:
    if reset and DB_DIR.exists():
        shutil.rmtree(DB_DIR)
    DB_DIR.mkdir(parents=True, exist_ok=True)

    chunks = chunk_documents(
        load_documents(), chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    client = chromadb.PersistentClient(path=str(DB_DIR))
    col = client.get_or_create_collection(name=COLLECTION, embedding_function=OllamaEF())
    if col.count() > 0:
        col.delete(ids=col.get()["ids"])

    ids = [f"{c.source}::{c.index}" for c in chunks]
    col.add(
        ids=ids,
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "doc_type": c.doc_type, "index": c.index} for c in chunks],
    )
    return col.count()


def retrieve(question: str, *, top_k: int = 4) -> list[dict]:
    if not DB_DIR.exists():
        raise FileNotFoundError("vector_db missing — run ingest first")
    client = chromadb.PersistentClient(path=str(DB_DIR))
    col = client.get_or_create_collection(name=COLLECTION, embedding_function=OllamaEF())
    if col.count() == 0:
        raise RuntimeError("empty collection — run ingest")
    res = col.query(query_texts=[question], n_results=min(top_k, col.count()))
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0]
    out: list[dict] = []
    for i, text in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        out.append(
            {
                "text": text,
                "source": meta.get("source", "?"),
                "doc_type": meta.get("doc_type", "?"),
                "distance": dists[i] if i < len(dists) else None,
            }
        )
    return out


def embed_model_name() -> str:
    return MODEL
