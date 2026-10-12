"""CLI smoke for lesson 09 — chunk the Fitllm knowledge-base."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.chunking import chunk_documents  # noqa: E402
from lib.kb import load_documents  # noqa: E402


def main() -> None:
    size = 800
    overlap = 150
    args = sys.argv[1:]
    if args and args[0].isdigit():
        size = int(args[0])
        if len(args) > 1 and args[1].isdigit():
            overlap = int(args[1])

    docs = load_documents()
    chunks = chunk_documents(docs, chunk_size=size, chunk_overlap=overlap)
    print(f"docs={len(docs)} chunks={len(chunks)} size={size} overlap={overlap}")
    by_type: dict[str, int] = {}
    for c in chunks:
        by_type[c.doc_type] = by_type.get(c.doc_type, 0) + 1
    print("by_type:", json.dumps(by_type, ensure_ascii=False))
    sample = chunks[0]
    print(f"sample source={sample.source} chars={len(sample.text)}")
    print(sample.text[:240].replace("\n", " ") + ("…" if len(sample.text) > 240 else ""))
    # overlap check: second chunk of same source should share a prefix with first tail
    same = [c for c in chunks if c.source == sample.source]
    if len(same) >= 2 and overlap > 0:
        tail = same[0].text[-min(40, overlap) :]
        ok = tail[:20] in same[1].text
        print(f"overlap_smoke={'ok' if ok else 'weak'} tail_in_next={ok}")


if __name__ == "__main__":
    main()
