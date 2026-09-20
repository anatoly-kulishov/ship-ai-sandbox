"""CLI smoke for lesson 04."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate import generate_plan  # noqa: E402
from lib.llm import provider_name  # noqa: E402


def main() -> None:
    brief = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "грудь и трицепс, 45 минут, только штанга и гантели"
    )
    print(f"provider={provider_name()}")
    result = generate_plan(brief)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    ids = [e["exerciseId"] for e in result["plan"]["exercises"]]
    print(f"exercises={len(ids)} ids={ids}")


if __name__ == "__main__":
    main()
