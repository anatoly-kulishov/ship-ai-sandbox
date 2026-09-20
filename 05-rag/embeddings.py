"""05 · RAG — embeddings + cosine retrieve over gym catalog.

Default: Ollama `nomic-embed-text` (GigaChat embeddings often 402 on PERS).
"""

from __future__ import annotations

import json
import math
import os
import re
from functools import lru_cache
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "catalog.fixture.json"
EMBEDDINGS_PATH = ROOT / "embeddings.fixture.json"

MODEL = (os.getenv("EMBEDDINGS_MODEL") or "nomic-embed-text").strip()
OLLAMA_BASE = (os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434/v1").rstrip("/").removesuffix(
    "/v1"
)


def load_catalog() -> list[dict]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def exercise_text(ex: dict) -> str:
    title = ex.get("name_ru") or ex.get("name") or ""
    return (
        f"{title} | {ex.get('body_part')} | {ex.get('target')} | "
        f"{ex.get('muscle_group')} | {ex.get('equipment')}"
    )


def cosine(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    if not n:
        return 0.0
    dot = na = nb = 0.0
    for i in range(n):
        x, y = a[i], b[i]
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0 or nb == 0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


def hints_from_brief(brief: str) -> list[str]:
    t = brief.lower()
    parts: list[str] = []
    rules: list[tuple[re.Pattern[str], list[str]]] = [
        (re.compile(r"груд|chest|pec"), ["chest"]),
        (re.compile(r"спин|back(?!ward)|тяга|крыл"), ["back"]),
        (re.compile(r"плеч|shoulder|дельт"), ["shoulders"]),
        (re.compile(r"трицеп|triceps"), ["upper arms"]),
        (re.compile(r"бицеп|biceps|бицух|банк[аиу]"), ["upper arms"]),
        (re.compile(r"рук[аиуеы]?|\barms?\b"), ["upper arms"]),
        (re.compile(r"ног|leg|квадр|ягод|glute|бедр|ляшк|галифе"), ["upper legs", "lower legs"]),
        (re.compile(r"пресс|core|waist|абдом"), ["waist"]),
        (re.compile(r"икр|calf"), ["lower legs"]),
    ]
    for rx, vals in rules:
        if rx.search(t):
            parts.extend(vals)
    return list(dict.fromkeys(parts))


def embed_ollama(texts: list[str]) -> list[list[float]]:
    out: list[list[float]] = []
    for prompt in texts:
        r = requests.post(
            f"{OLLAMA_BASE}/api/embeddings",
            json={"model": MODEL, "prompt": prompt},
            timeout=60,
        )
        r.raise_for_status()
        emb = r.json().get("embedding")
        if not isinstance(emb, list):
            raise RuntimeError("ollama embeddings: missing embedding")
        out.append(emb)
    return out


def embed(texts: list[str]) -> list[list[float]]:
    # Default Ollama — GigaChat /embeddings is often 402 on PERS.
    if (os.getenv("EMBEDDINGS_PROVIDER") or "ollama").strip().lower() == "gigachat":
        from lib.llm import BASE_URL, fetch_access_token

        token = fetch_access_token()
        ssl = str(os.getenv("GIGACHAT_SSL_VERIFY", "false")).lower() in {"1", "true", "yes"}
        model = os.getenv("EMBEDDINGS_MODEL") or "Embeddings"
        r = requests.post(
            f"{BASE_URL}/embeddings",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"model": model, "input": texts},
            verify=ssl,
            timeout=60,
        )
        if r.status_code >= 400:
            return embed_ollama(texts)
        rows = sorted(r.json().get("data") or [], key=lambda d: d.get("index", 0))
        return [row["embedding"] for row in rows]
    return embed_ollama(texts)


@lru_cache(maxsize=1)
def load_embedding_index() -> dict:
    if not EMBEDDINGS_PATH.exists():
        return {"provider": "none", "model": MODEL, "dims": 0, "items": []}
    return json.loads(EMBEDDINGS_PATH.read_text(encoding="utf-8"))


def build_embedding_index(catalog: list[dict] | None = None) -> dict:
    catalog = catalog or load_catalog()
    texts = [exercise_text(ex) for ex in catalog]
    vecs = embed(texts)
    items = [
        {"id": catalog[i]["id"], "vec": [round(x, 4) for x in vecs[i]]}
        for i in range(len(catalog))
    ]
    payload = {
        "provider": "ollama",
        "model": MODEL,
        "dims": len(vecs[0]) if vecs else 0,
        "items": items,
    }
    EMBEDDINGS_PATH.write_text(json.dumps(payload), encoding="utf-8")
    load_embedding_index.cache_clear()
    return payload


def retrieve(brief: str, top_k: int = 20) -> list[dict]:
    catalog = load_catalog()
    by_id = {ex["id"]: ex for ex in catalog}
    index = load_embedding_index()
    items = index.get("items") or []
    parts = hints_from_brief(brief)
    expanded = f"{brief} | {' '.join(parts)}" if parts else brief

    if not items:
        pool = (
            [ex for ex in catalog if ex.get("body_part") in parts]
            if parts
            else catalog
        )
        ranked = sorted(pool or catalog, key=lambda e: e.get("globalPopularity") or 25, reverse=True)
        return ranked[:top_k]

    q = embed([expanded])[0]
    scored: list[tuple[float, dict]] = []
    for row in items:
        ex = by_id.get(row["id"])
        if not ex:
            continue
        if parts and ex.get("body_part") not in parts:
            continue
        scored.append((cosine(q, row["vec"]), ex))
    scored.sort(key=lambda x: x[0], reverse=True)
    if len(scored) < top_k and parts:
        have = {ex["id"] for _, ex in scored}
        for ex in sorted(catalog, key=lambda e: e.get("globalPopularity") or 25, reverse=True):
            if ex["id"] in have:
                continue
            if ex.get("body_part") not in parts:
                continue
            scored.append((0.0, ex))
            if len(scored) >= top_k:
                break
    return [ex for _, ex in scored[:top_k]]
