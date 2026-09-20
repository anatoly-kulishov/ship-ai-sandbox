"""CLI smoke for lesson 05 — build / embed / retrieve."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from embeddings import (  # noqa: E402
    build_embedding_index,
    embed,
    load_embedding_index,
    retrieve,
)
from lib.llm import MODEL, provider_name  # noqa: E402


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args and args[0] in {"build", "embed", "retrieve"} else "retrieve"
    rest = args[1:] if args and args[0] in {"build", "embed", "retrieve"} else args

    if cmd == "build":
        payload = build_embedding_index()
        print(f"wrote embeddings.fixture.json items={len(payload['items'])} dims={payload['dims']}")
        return

    if cmd == "embed":
        text = " ".join(rest) or "сгибание на бицепс"
        vec = embed([text])[0]
        print(json.dumps({"dims": len(vec), "head": [round(x, 5) for x in vec[:8]]}, ensure_ascii=False))
        return

    brief = " ".join(rest) or "хочу накачать банки"
    index = load_embedding_index()
    if not index.get("items"):
        print("embeddings.fixture.json empty — building…")
        build_embedding_index()

    print(f"provider_chat={provider_name()} model_chat={MODEL}")
    hits = retrieve(brief, top_k=10)
    print(f"brief={brief!r} top={len(hits)}")
    for i, ex in enumerate(hits, 1):
        title = ex.get("name_ru") or ex.get("name")
        print(f"{i:2}. {ex['id']} | {title} | {ex['body_part']} | {ex['target']}")


if __name__ == "__main__":
    main()
