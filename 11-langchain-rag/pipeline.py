"""Thin LangChain RAG over the same Fitllm knowledge-base."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.kb import load_documents
from lib.llm import AUTH_KEY, BASE_URL, MODEL, fetch_access_token, provider_name
from lib.ollama_embed import embed_texts

DB_DIR = Path(__file__).resolve().parent / "vector_db_lc"
COLLECTION = "fitllm_lc"

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Ты knowledge-worker Fitllm. Отвечай только по CONTEXT. "
            "Если ответа нет — скажи «не знаю по базе Fitllm». Кратко, по-русски. "
            "Укажи source, если уместно.\n\nCONTEXT:\n{context}",
        ),
        ("human", "{question}"),
    ]
)


class OllamaEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return embed_texts(texts)

    def embed_query(self, text: str) -> list[float]:
        return embed_texts([text])[0]


def _llm() -> ChatOpenAI:
    key = AUTH_KEY or "ollama"
    if provider_name() == "gigachat":
        key = fetch_access_token()
    return ChatOpenAI(
        base_url=BASE_URL,
        api_key=key,
        model=MODEL,
        temperature=0,
    )


def ingest(*, chunk_size: int = 800, chunk_overlap: int = 150) -> int:
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)
    DB_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_documents()
    docs = [
        Document(page_content=d.text, metadata={"source": d.source, "doc_type": d.doc_type})
        for d in raw
    ]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    store = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(),
        persist_directory=str(DB_DIR),
        collection_name=COLLECTION,
    )
    return store._collection.count()


def _store() -> Chroma:
    if not DB_DIR.exists():
        raise FileNotFoundError("vector_db_lc missing — run ingest")
    return Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=OllamaEmbeddings(),
        collection_name=COLLECTION,
    )


def ask(question: str, *, top_k: int = 4) -> dict:
    store = _store()
    hits = store.similarity_search(question, k=top_k)
    if not hits:
        return {
            "answer": "не знаю по базе Fitllm",
            "hits": [],
            "provider": provider_name(),
            "model": MODEL,
        }
    context = "\n\n".join(
        f"[{d.metadata.get('source', '?')}]\n{d.page_content}" for d in hits
    )
    chain = PROMPT | _llm()
    msg = chain.invoke({"context": context, "question": question})
    text = getattr(msg, "content", str(msg)).strip()
    return {
        "answer": text,
        "hits": [
            {
                "source": d.metadata.get("source"),
                "doc_type": d.metadata.get("doc_type"),
                "text": d.page_content,
            }
            for d in hits
        ],
        "provider": provider_name(),
        "model": MODEL,
    }
