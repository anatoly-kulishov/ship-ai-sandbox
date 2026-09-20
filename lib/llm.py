"""OpenAI-compatible LLM client with dual profiles in .env.

Switch provider without rewriting keys:

    LLM_PROVIDER=gigachat   # or ollama
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

PROVIDER = (os.getenv("LLM_PROVIDER") or "gigachat").strip().lower()


def _cfg() -> dict[str, str]:
    if PROVIDER == "ollama":
        return {
            "base_url": (os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434/v1").rstrip("/"),
            "model": os.getenv("OLLAMA_MODEL") or "qwen2.5:3b",
            "api_key": (os.getenv("OLLAMA_API_KEY") or "ollama").removeprefix("sk-"),
        }
    if PROVIDER in {"gigachat", "giga"}:
        return {
            "base_url": (os.getenv("GIGACHAT_BASE_URL") or "https://api.giga.chat/v1").rstrip("/"),
            "model": os.getenv("GIGACHAT_MODEL") or "GigaChat-2",
            "api_key": (os.getenv("GIGACHAT_API_KEY") or os.getenv("LLM_API_KEY") or "").removeprefix("sk-"),
            "oauth_url": os.getenv("GIGACHAT_OAUTH_URL")
            or "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            "scope": os.getenv("GIGACHAT_SCOPE") or "GIGACHAT_API_PERS",
            "ssl_verify": os.getenv("GIGACHAT_SSL_VERIFY", "false"),
        }
    # generic OpenAI-compatible fallback (legacy LLM_* still works)
    return {
        "base_url": (os.getenv("LLM_BASE_URL") or "https://api.giga.chat/v1").rstrip("/"),
        "model": os.getenv("LLM_MODEL") or "GigaChat-2",
        "api_key": (os.getenv("LLM_API_KEY") or "").removeprefix("sk-"),
    }


_CFG = _cfg()
BASE_URL = _CFG["base_url"]
MODEL = _CFG["model"]
AUTH_KEY = _CFG["api_key"]


def provider_name() -> str:
    if PROVIDER in {"ollama", "gigachat", "giga"}:
        return "gigachat" if PROVIDER == "giga" else PROVIDER
    u = BASE_URL.lower()
    if "11434" in u or "ollama" in u:
        return "ollama"
    if "giga.chat" in u or "sberbank" in u:
        return "gigachat"
    return "openai_compatible"


def _is_gigachat() -> bool:
    return provider_name() == "gigachat"


def fetch_access_token() -> str:
    if not AUTH_KEY:
        raise SystemExit("Missing GIGACHAT_API_KEY in .env")
    ssl_verify = str(_CFG.get("ssl_verify", "false")).lower() in {"1", "true", "yes"}
    response = requests.post(
        _CFG.get("oauth_url") or "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {AUTH_KEY}",
        },
        data={"scope": _CFG.get("scope") or "GIGACHAT_API_PERS"},
        timeout=30,
        verify=ssl_verify,
    )
    if not response.ok:
        raise SystemExit(f"GigaChat OAuth failed ({response.status_code}): {response.text[:500]}")
    token = response.json().get("access_token")
    if not token:
        raise SystemExit(f"GigaChat OAuth: no access_token in {response.text[:500]}")
    return token


def get_client() -> OpenAI:
    if _is_gigachat():
        return OpenAI(api_key=fetch_access_token(), base_url=BASE_URL)
    return OpenAI(api_key=AUTH_KEY or "ollama", base_url=BASE_URL)


def ping() -> dict:
    name = provider_name()
    if name == "ollama":
        root = BASE_URL.replace("/v1", "")
        r = requests.get(f"{root}/api/tags", timeout=5)
        r.raise_for_status()
        models = [m.get("name") for m in r.json().get("models", [])]
        return {"provider": name, "ok": True, "models": models, "model": MODEL}
    client = get_client()
    client.models.list()
    return {"provider": name, "ok": True, "model": MODEL}
