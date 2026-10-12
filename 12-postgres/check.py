"""CLI smoke for lesson 12 — schema, classify log, list events."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import init_schema, list_events, log_event, ping  # noqa: E402


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "smoke"

    if cmd == "ping":
        print(json.dumps(ping(), ensure_ascii=False, indent=2))
        return

    if cmd == "init":
        init_schema()
        print("schema ok")
        return

    if cmd == "list":
        kind = args[1] if len(args) > 1 else None
        print(json.dumps(list_events(kind=kind, limit=10), ensure_ascii=False, indent=2))
        return

    # smoke: ping + init + synthetic event (no LLM) + optional classify
    print("ping:", ping())
    init_schema()
    demo = log_event(
        "smoke",
        brief="hello postgres",
        payload={"ok": True, "lesson": 12},
    )
    print("logged:", json.dumps(demo, ensure_ascii=False))
    print("recent:", json.dumps(list_events(limit=3), ensure_ascii=False, indent=2))

    if "--llm" in args:
        try:
            from server import NoteIn, classify

            out = classify(NoteIn(text="сегодня купить хлеб"))
            print("classify:", json.dumps(out, ensure_ascii=False, indent=2))
        except Exception as llm_exc:  # noqa: BLE001
            print(f"llm_skip: {llm_exc}", file=sys.stderr)
            print("Postgres path OK — включи Ollama/GigaChat для --llm")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}", file=sys.stderr)
        print(
            "Hint: start Postgres (`npm run postgres:up`) and set DATABASE_URL in .env",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
