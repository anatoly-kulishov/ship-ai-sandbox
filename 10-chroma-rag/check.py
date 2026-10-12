"""CLI smoke for lesson 10 — ingest / retrieve / ask."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from answer import answer  # noqa: E402
from store import embed_model_name, ingest, retrieve  # noqa: E402


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args and args[0] in {"ingest", "retrieve", "ask"} else "ask"
    rest = args[1:] if args and args[0] in {"ingest", "retrieve", "ask"} else args

    if cmd == "ingest":
        n = ingest()
        print(f"ingested count={n} embed={embed_model_name()}")
        return

    q = " ".join(rest) or "Что такое Draftllm?"
    if cmd == "retrieve":
        try:
            hits = retrieve(q)
        except (FileNotFoundError, RuntimeError):
            print("ingest…")
            ingest()
            hits = retrieve(q)
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return

    try:
        result = answer(q)
    except (FileNotFoundError, RuntimeError):
        print("ingest…")
        ingest()
        result = answer(q)
    print(f"provider={result['provider']} model={result['model']}")
    print("hits:", [h["source"] for h in result["hits"]])
    print(result["answer"])


if __name__ == "__main__":
    main()
