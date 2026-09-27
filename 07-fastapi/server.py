"""07 · FastAPI gateway — HTTP layer over the gym plan generator and RAG retrieve.

Skills: FastAPI, Pydantic request/response contracts, error mapping, Swagger.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]


def _load_module(relative_path: str, name: str) -> object:
    file_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Reuse the business logic from previous lessons without copying code.
gym_generate = _load_module("04-gym-plan/generate.py", "gym_generate")
rag_embeddings = _load_module("05-rag/embeddings.py", "rag_embeddings")

# LLM provider utilities for the health endpoint.
sys.path.insert(0, str(ROOT))
from lib.llm import MODEL, ping, provider_name  # noqa: E402

app = FastAPI(
    title="ship-ai-sandbox · FastAPI gateway",
    description="LLM-backed endpoints: gym plan generation and RAG retrieve.",
    version="0.1.0",
)


@app.exception_handler(ValueError)
async def _value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


class BriefIn(BaseModel):
    brief: str = Field(
        min_length=1,
        max_length=1000,
        description="Описание тренировки: зоны, оборудование, время.",
    )


class RetrieveIn(BaseModel):
    brief: str = Field(
        min_length=1,
        max_length=1000,
        description="Запрос по смыслу для поиска упражнений.",
    )
    top_k: int = Field(default=10, ge=1, le=50, description="Сколько упражнений вернуть.")


class HealthOut(BaseModel):
    status: str
    provider: str
    model: str


@app.get("/health", response_model=HealthOut)
def health() -> dict:
    try:
        info = ping()
        return {
            "status": "ok",
            "provider": info.get("provider", provider_name()),
            "model": info.get("model", MODEL),
        }
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=503, detail=f"Provider unavailable: {exc}") from exc


@app.post("/plan")
def plan(body: BriefIn) -> dict:
    try:
        return gym_generate.generate_plan(body.brief)
    except HTTPException:
        raise
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=502, detail=f"Generation failed: {exc}") from exc


@app.post("/retrieve")
def retrieve(body: RetrieveIn) -> list[dict]:
    try:
        return rag_embeddings.retrieve(body.brief, top_k=body.top_k)
    except HTTPException:
        raise
    except (Exception, SystemExit) as exc:
        raise HTTPException(status_code=502, detail=f"Retrieve failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8600, reload=True)
