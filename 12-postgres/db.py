"""Postgres access for lesson 12 — dialog/event log."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=True)

DEFAULT_URL = "postgresql://ship:ship@127.0.0.1:5432/ship_ai"


def database_url() -> str:
    return (os.getenv("DATABASE_URL") or DEFAULT_URL).strip()


@contextmanager
def connect() -> Iterator[psycopg.Connection]:
    with psycopg.connect(database_url(), row_factory=dict_row) as conn:
        yield conn


def ping() -> dict[str, Any]:
    with connect() as conn:
        row = conn.execute("SELECT version() AS version, current_database() AS db").fetchone()
        assert row is not None
        return {"db": row["db"], "version": row["version"].split(",")[0]}


def init_schema() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id          BIGSERIAL PRIMARY KEY,
                kind        TEXT NOT NULL,
                brief       TEXT NOT NULL DEFAULT '',
                payload     JSONB NOT NULL DEFAULT '{}'::jsonb,
                created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS events_kind_created_idx
            ON events (kind, created_at DESC)
            """
        )
        conn.commit()


def log_event(kind: str, *, brief: str = "", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    body = payload or {}
    with connect() as conn:
        row = conn.execute(
            """
            INSERT INTO events (kind, brief, payload)
            VALUES (%s, %s, %s::jsonb)
            RETURNING id, kind, brief, payload, created_at
            """,
            (kind, brief, json.dumps(body, ensure_ascii=False)),
        ).fetchone()
        conn.commit()
        assert row is not None
        return _serialize(row)


def list_events(*, kind: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    limit = max(1, min(int(limit), 100))
    with connect() as conn:
        if kind:
            rows = conn.execute(
                """
                SELECT id, kind, brief, payload, created_at
                FROM events
                WHERE kind = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (kind, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, kind, brief, payload, created_at
                FROM events
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,),
            ).fetchall()
    return [_serialize(r) for r in rows]


def _serialize(row: dict[str, Any]) -> dict[str, Any]:
    created = row["created_at"]
    if isinstance(created, datetime):
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        created_s = created.isoformat()
    else:
        created_s = str(created)
    payload = row["payload"]
    if isinstance(payload, str):
        payload = json.loads(payload)
    return {
        "id": row["id"],
        "kind": row["kind"],
        "brief": row["brief"],
        "payload": payload,
        "created_at": created_s,
    }
