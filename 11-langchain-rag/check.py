"""CLI smoke for lesson 11 — LangChain RAG."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import ask, ingest  # noqa: E402


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args and args[0] in {"ingest", "ask"} else "ask"
    rest = args[1:] if args and args[0] in {"ingest", "ask"} else args

    if cmd == "ingest":
        n = ingest()
        print(f"ingested count={n}")
        return

    q = " ".join(rest) or "Зачем нужен whitelist id?"
    try:
        result = ask(q)
    except FileNotFoundError:
        print("ingest…")
        ingest()
        result = ask(q)
    print(f"provider={result['provider']} model={result['model']}")
    print("hits:", [h["source"] for h in result["hits"]])
    print(result["answer"])


if __name__ == "__main__":
    main()
