"""Recursive character splitter (LangChain-style, no dependency).

Ideas from Ed Donner w5 / RecursiveCharacterTextSplitter — MIT curriculum.
"""

from __future__ import annotations

from dataclasses import dataclass

from lib.kb import Document


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str
    doc_type: str
    index: int


DEFAULT_SEPARATORS = ["\n\n", "\n", " ", ""]


def recursive_split(
    text: str,
    *,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
    separators: list[str] | None = None,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and < chunk_size")

    seps = separators if separators is not None else DEFAULT_SEPARATORS
    pieces = _split_text(text.strip(), chunk_size, seps)
    if chunk_overlap <= 0 or len(pieces) <= 1:
        return pieces
    return _apply_overlap(pieces, chunk_size, chunk_overlap)


def _split_text(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    sep = separators[0] if separators else ""
    rest = separators[1:] if len(separators) > 1 else [""]
    parts = list(text) if sep == "" else [p for p in text.split(sep) if p]

    chunks: list[str] = []
    buf = ""
    join = sep

    for part in parts:
        candidate = part if not buf else f"{buf}{join}{part}"
        if len(candidate) <= chunk_size:
            buf = candidate
            continue
        if buf.strip():
            chunks.append(buf.strip())
            buf = ""
        if len(part) <= chunk_size:
            buf = part
        else:
            chunks.extend(_split_text(part, chunk_size, rest))
    if buf.strip():
        chunks.append(buf.strip())
    return chunks


def _apply_overlap(pieces: list[str], chunk_size: int, overlap: int) -> list[str]:
    """Prefix each chunk (except first) with the tail of the previous final chunk."""
    out: list[str] = [pieces[0]]
    for piece in pieces[1:]:
        tail = out[-1][-overlap:]
        merged = f"{tail}\n{piece}".strip()
        # ponytail: ceiling — rare merge > chunk_size+overlap; trim head if needed
        if len(merged) > chunk_size + overlap:
            merged = merged[-chunk_size - overlap :]
        out.append(merged)
    return out


def chunk_documents(
    documents: list[Document],
    *,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Chunk]:
    result: list[Chunk] = []
    for doc in documents:
        pieces = recursive_split(doc.text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for i, piece in enumerate(pieces):
            result.append(
                Chunk(text=piece, source=doc.source, doc_type=doc.doc_type, index=i)
            )
    return result
