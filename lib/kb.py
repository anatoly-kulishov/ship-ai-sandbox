"""Load markdown knowledge-base for RAG lessons 09–11."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge-base"


@dataclass(frozen=True)
class Document:
    text: str
    source: str
    doc_type: str


def load_documents(kb_dir: Path | None = None) -> list[Document]:
    root = kb_dir or KB_DIR
    docs: list[Document] = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        doc_type = rel.parts[0] if len(rel.parts) > 1 else "root"
        docs.append(
            Document(
                text=path.read_text(encoding="utf-8"),
                source=str(rel).replace("\\", "/"),
                doc_type=doc_type,
            )
        )
    return docs
