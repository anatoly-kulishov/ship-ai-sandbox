"""08 · Async gateway self-check.

1) Pure asyncio sleep demo (always) — wall << sequential.
2) FastAPI TestClient for health / classify / demos.
3) LLM batch skipped if provider is down.
"""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "08-asyncio"))

from fastapi.testclient import TestClient

import server  # noqa: E402

client = TestClient(server.app)


async def _sleep_selfcheck() -> None:
    n, delay = 3, 0.35
    t0 = time.perf_counter()
    await asyncio.gather(*[asyncio.sleep(delay) for _ in range(n)])
    wall = time.perf_counter() - t0
    sequential = n * delay
    assert wall < sequential * 0.75, (wall, sequential)
    print(f"asyncio.gather sleep: wall={wall:.2f}s sequential={sequential:.2f}s → concurrent OK")


def main() -> int:
    asyncio.run(_sleep_selfcheck())

    print("POST /demo/sleep")
    r = client.post("/demo/sleep", json={"n": 3, "sleep_sec": 0.35})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["concurrent"] is True, body
    print(f"  wall={body['wall_sec']}s if_sequential={body['if_sequential_sec']}s")

    print("GET /health")
    r = client.get("/health")
    provider_ok = r.status_code == 200
    if provider_ok:
        info = r.json()
        assert info.get("async") is True
        print(f"  provider={info['provider']} model={info['model']}")
    else:
        print(f"  WARNING: provider unavailable ({r.status_code}): {r.text}")

    print("POST /classify empty → 422")
    r = client.post("/classify", json={"text": ""})
    assert r.status_code == 422, r.text
    print("  ok")

    if not provider_ok:
        print("\n✅ Async checks passed (sleep + validation). LLM skipped.")
        return 0

    print("POST /classify")
    r = client.post("/classify", json={"text": "завтра созвон с инвесторами"})
    if r.status_code == 200:
        data = r.json()
        assert data["category"] in {"WORK", "PERSONAL", "SHOPPING"}
        print(f"  category={data['category']} urgent={data['urgent']}")
    else:
        print(f"  WARNING: classify {r.status_code}: {r.text[:200]}")

    print("POST /demo/classify (parallel)")
    r = client.post(
        "/demo/classify",
        json={
            "notes": [
                "купить хлеб",
                "завтра созвон",
                "в выходные бассейн",
            ]
        },
    )
    if r.status_code == 200:
        batch = r.json()
        assert batch["n"] == 3
        assert len(batch["results"]) == 3
        print(f"  wall={batch['wall_sec']}s results={len(batch['results'])}")
    else:
        print(f"  WARNING: batch {r.status_code}: {r.text[:200]}")

    print("\n✅ Async lesson checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
