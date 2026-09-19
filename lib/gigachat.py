"""Shared GigaChat OpenAI-compatible client."""

from __future__ import annotations

import os
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

AUTH_KEY = (os.getenv("LLM_API_KEY") or "").removeprefix("sk-")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.giga.chat/v1")
MODEL = os.getenv("LLM_MODEL", "GigaChat-2")
OAUTH_URL = os.getenv(
    "LLM_OAUTH_URL",
    "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
)
SCOPE = os.getenv("LLM_SCOPE", "GIGACHAT_API_PERS")
SSL_VERIFY = os.getenv("LLM_SSL_VERIFY", "false").lower() in {"1", "true", "yes"}


def fetch_access_token() -> str:
    if not AUTH_KEY:
        raise SystemExit("Missing LLM_API_KEY in .env")
    response = requests.post(
        OAUTH_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {AUTH_KEY}",
        },
        data={"scope": SCOPE},
        timeout=30,
        verify=SSL_VERIFY,
    )
    if not response.ok:
        raise SystemExit(f"GigaChat OAuth failed ({response.status_code}): {response.text[:500]}")
    token = response.json().get("access_token")
    if not token:
        raise SystemExit(f"GigaChat OAuth: no access_token in {response.text[:500]}")
    return token


def get_client() -> OpenAI:
    return OpenAI(api_key=fetch_access_token(), base_url=BASE_URL)
