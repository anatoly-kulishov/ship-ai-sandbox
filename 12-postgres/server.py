"""12 · FastAPI + Postgres — log classify / plan / rag asks."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from db import init_schema, list_events, log_event, ping  # noqa: E402
from lib.llm import MODEL, provider_name  # noqa: E402


def _load(relative: str, name: str) -> Any:
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


categorize = _load("01-note-sorter/categorize.py", "pg_categorize")
gym_generate = _load("04-gym-plan/generate.py", "pg_gym_generate")

app = FastAPI(
    title="ship-ai-sandbox · Postgres gateway",
    description="LLM calls + durable event log in PostgreSQL.",
    version="0.1.0",
)


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class BriefIn(BaseModel):
    brief: str = Field(min_length=1, max_length=1000)


@app.on_event("startup")
def _startup() -> None:
    try:
        init_schema()
    except Exception as exc:  # noqa: BLE001 — show in /health
        app.state.db_error = str(exc)
    else:
        app.state.db_error = None


@app.get("/health")
def health() -> dict[str, Any]:
    err = getattr(app.state, "db_error", None)
    try:
        db = ping()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Postgres unavailable: {exc}") from exc
    return {
        "status": "ok" if not err else "degraded",
        "provider": provider_name(),
        "model": MODEL,
        "postgres": db,
        "schema_error": err,
    }


@app.post("/classify")
def classify(body: NoteIn) -> dict[str, Any]:
    try:
        result = categorize.categorize_note(body.text)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"LLM failed: {exc}") from exc
    payload = result.model_dump() if hasattr(result, "model_dump") else dict(result)
    event = log_event("classify", brief=body.text, payload=payload)
    return {"result": payload, "event": event}


@app.post("/plan")
def plan(body: BriefIn) -> dict[str, Any]:
    try:
        result = gym_generate.generate_plan(body.brief)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Plan failed: {exc}") from exc
    event = log_event("plan", brief=body.brief, payload=result)
    return {"result": result, "event": event}


@app.get("/events")
def events(kind: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    try:
        return list_events(kind=kind, limit=limit)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"Postgres unavailable: {exc}") from exc
