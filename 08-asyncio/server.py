"""08 · Async FastAPI gateway — AsyncOpenAI + concurrent requests.

Why async: LLM calls wait on the network. Sync handlers block one worker
per request; async handlers free the event loop while awaiting I/O.
"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "08-asyncio"))

from classify import categorize_note_async  # noqa: E402
from lib.llm import MODEL, ping_async, provider_name  # noqa: E402


def _load_module(relative_path: str, name: str) -> object:
    file_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gym_generate = _load_module("04-gym-plan/generate.py", "gym_generate_async_lesson")

app = FastAPI(
    title="ship-ai-sandbox · async gateway",
    description="AsyncOpenAI + concurrent demos. Sync plan via asyncio.to_thread.",
    version="0.1.0",
)


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class BriefIn(BaseModel):
    brief: str = Field(min_length=1, max_length=1000)


class ConcurrentIn(BaseModel):
    n: int = Field(default=3, ge=2, le=8, description="How many parallel sleeps")
    sleep_sec: float = Field(default=0.4, ge=0.1, le=2.0)


class ClassifyBatchIn(BaseModel):
    notes: list[str] = Field(min_length=2, max_length=6)


@app.get("/health")
async def health() -> dict:
    try:
        info = await ping_async()
        return {
            "status": "ok",
            "provider": info.get("provider", provider_name()),
            "model": info.get("model", MODEL),
            "async": True,
        }
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=503, detail=f"Provider unavailable: {exc}") from exc


@app.post("/classify")
async def classify(body: NoteIn) -> dict:
    try:
        result = await categorize_note_async(body.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=502, detail=f"Classify failed: {exc}") from exc
    return {"ok": True, "provider": provider_name(), "model": MODEL, **result.model_dump()}


@app.post("/plan")
async def plan(body: BriefIn) -> dict:
    # Sync generate_plan stays as-is; to_thread keeps the event loop free.
    try:
        return await asyncio.to_thread(gym_generate.generate_plan, body.brief)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=502, detail=f"Generation failed: {exc}") from exc


@app.post("/demo/sleep")
async def demo_sleep(body: ConcurrentIn) -> dict:
    """n parallel sleeps: wall time ≈ sleep_sec, not n × sleep_sec."""
    t0 = time.perf_counter()
    await asyncio.gather(*[asyncio.sleep(body.sleep_sec) for _ in range(body.n)])
    wall = round(time.perf_counter() - t0, 3)
    sequential = round(body.n * body.sleep_sec, 3)
    return {
        "n": body.n,
        "sleep_sec": body.sleep_sec,
        "wall_sec": wall,
        "if_sequential_sec": sequential,
        "concurrent": wall < sequential * 0.75,
    }


@app.post("/demo/classify")
async def demo_classify(body: ClassifyBatchIn) -> dict:
    """n parallel AsyncOpenAI classify calls — gateway stays non-blocking."""
    t0 = time.perf_counter()
    try:
        results = await asyncio.gather(
            *[categorize_note_async(note) for note in body.notes]
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=502, detail=f"Batch classify failed: {exc}") from exc
    wall = round(time.perf_counter() - t0, 3)
    return {
        "n": len(body.notes),
        "wall_sec": wall,
        "results": [r.model_dump() for r in results],
        "note": "wall ≈ slowest call if gateway+provider allow overlap; model may still serialize",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8601, reload=True)
