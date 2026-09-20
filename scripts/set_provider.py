#!/usr/bin/env python3
"""Flip LLM_PROVIDER in .env without touching other keys."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
ALLOWED = {"gigachat", "ollama"}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ALLOWED:
        raise SystemExit(f"Usage: {sys.argv[0]} [{'|'.join(sorted(ALLOWED))}]")
    provider = sys.argv[1]
    if not ENV.exists():
        raise SystemExit(f"Missing {ENV} — copy from .env.example")

    text = ENV.read_text()
    if re.search(r"(?m)^LLM_PROVIDER=", text):
        text = re.sub(r"(?m)^LLM_PROVIDER=.*$", f"LLM_PROVIDER={provider}", text)
    else:
        text = f"LLM_PROVIDER={provider}\n" + text
    ENV.write_text(text)
    print(f"LLM_PROVIDER={provider}")


if __name__ == "__main__":
    main()
