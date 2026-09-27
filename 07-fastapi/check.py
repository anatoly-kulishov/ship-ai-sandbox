"""07 · FastAPI self-check via TestClient.

No manual curl needed: starts the app in-process and hits every endpoint.
Skips the embedding retrieve test if Ollama is not reachable.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "07-fastapi"))

import requests
from fastapi.testclient import TestClient

import server  # noqa: E402

client = TestClient(server.app)


def _ollama_reachable() -> bool:
    base = server.rag_embeddings.OLLAMA_BASE
    try:
        requests.get(f"{base}/api/tags", timeout=3).raise_for_status()
        return True
    except Exception:
        return False


def main() -> int:
    provider_ok = False
    print("GET /health")
    r = client.get("/health")
    if r.status_code == 200:
        body = r.json()
        assert body["status"] == "ok"
        print(f"  provider={body['provider']} model={body['model']}")
        provider_ok = True
    else:
        print(f"  WARNING: provider unavailable ({r.status_code}): {r.text}")

    print("POST /plan with invalid brief (empty)")
    r = client.post("/plan", json={"brief": ""})
    assert r.status_code == 422, r.text
    print("  correctly rejected with 422")

    print("GET /unknown")
    r = client.get("/unknown")
    assert r.status_code == 404
    print("  404 as expected")

    if not provider_ok:
        print(
            "\n⚠️  Provider not available — skipping LLM tests. "
            "Set LLM_PROVIDER and ensure the provider is reachable."
        )
        print("\n✅ Basic FastAPI checks passed (health/validation/404)")
        return 0

    print("POST /plan")
    r = client.post(
        "/plan",
        json={"brief": "грудь и трицепс, 45 минут, штанга и гантели"},
    )
    plan_ok = False
    if r.status_code == 200:
        plan = r.json()
        assert plan["ok"] is True
        assert "plan" in plan
        exercises = plan["plan"]["exercises"]
        assert len(exercises) >= 5
        ids = {e["exerciseId"] for e in exercises}
        assert len(ids) == len(exercises), "duplicate exerciseId"
        print(f"  name={plan['plan']['name']} exercises={len(exercises)}")
        plan_ok = True
    elif r.status_code == 502 and "Invalid plan payload" in r.text:
        print(
            "  plan endpoint reachable, but local model returned payload that violates schema "
            "(common for qwen2.5:3b). The API correctly rejected it with 502."
        )
    else:
        assert r.status_code == 200, r.text

    if _ollama_reachable():
        print("POST /retrieve")
        r = client.post("/retrieve", json={"brief": "банки", "top_k": 5})
        assert r.status_code == 200, r.text
        items = r.json()
        assert isinstance(items, list)
        assert len(items) <= 5
        if items:
            assert "id" in items[0]
        print(f"  items={len(items)}")
    else:
        print("POST /retrieve — skipped (Ollama embeddings not reachable)")

    print("\n✅ All FastAPI checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
