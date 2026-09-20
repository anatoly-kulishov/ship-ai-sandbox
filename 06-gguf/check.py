"""06 · GGUF / quantization.

Skill: estimate RAM for Q4/Q5/Q8 and pick a local model that fits.
Does not pull weights. Market: on-prem inference, hardware-aware model choice.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from recommend import CATALOG, estimate_ram_gb, pick, report, usable_gb  # noqa: E402


def _selfcheck() -> None:
    assert estimate_ram_gb(7, "q4") < estimate_ram_gb(7, "q5")
    assert estimate_ram_gb(7, "q5") < estimate_ram_gb(7, "q8")
    assert estimate_ram_gb(7, "q8") < estimate_ram_gb(7, "fp16")
    assert estimate_ram_gb(7, "q4") < estimate_ram_gb(14, "q4")

    def choice(total: float) -> dict:
        return pick(CATALOG, usable_gb(total))

    s8 = choice(8)
    assert s8["recommended"] is not None
    assert s8["recommended"].tag == "qwen2.5:3b"
    assert s8["sandbox"].tag == "qwen2.5:3b"

    s16 = choice(16)
    assert s16["recommended"].tag == "qwen2.5:7b"
    assert s16["stretch"].tag == "qwen2.5:14b"
    assert s16["sandbox"].tag == "qwen2.5:7b"

    s24 = choice(24)
    assert s24["recommended"].tag == "qwen2.5:14b"
    assert s24["stretch"].tag == "qwen2.5:14b"
    assert s24["sandbox"].tag == "qwen2.5:7b"

    s32 = choice(32)
    assert s32["recommended"].tag == "qwen2.5:32b"

    s64 = choice(64)
    assert s64["recommended"].tag == "llama3.1:70b"

    for total in (8, 16, 24, 32, 64):
        u = usable_gb(total)
        for model in choice(total).values():
            if model is not None:
                assert model.ram_gb <= u + 1e-9, (total, model.tag, model.ram_gb, u)


def main() -> None:
    _selfcheck()
    payload = report()
    print("selfcheck: ok")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    rec = payload["recommended"]
    sandbox = payload["sandbox"]
    names = {item["name"] for item in payload["installed"]}
    print()
    print(f"RAM {payload['hardware']['ram_gb']} GB · {payload['hardware']['chip']}")
    print(f"usable {payload['usable_gb']} GB (OS reserve {payload['os_reserve_gb']})")
    print(f"recommended (comfortable): {rec}")
    print(f"sandbox JSON default:      {sandbox}")
    if sandbox and sandbox not in names and f"{sandbox}:latest" not in names:
        print(f"optional: ollama pull {sandbox}   # не обязательно для этого урока")


if __name__ == "__main__":
    main()
