"""03 · Local LLM with Ollama.

Skill: run the same OpenAI-compatible code against a local model
(no cloud API). Market: on-prem / offline inference basics.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "01-note-sorter"))

from categorize import categorize_note, format_result  # noqa: E402
from lib.llm import MODEL, BASE_URL, ping, provider_name  # noqa: E402


def main() -> None:
    print(f"provider: {provider_name()}")
    print(f"base_url: {BASE_URL}")
    print(f"model:    {MODEL}")
    try:
        info = ping()
    except Exception as e:
        raise SystemExit(
            "Ollama не отвечает. Установи и запусти:\n"
            "  brew install ollama && ollama serve\n"
            "  ollama pull qwen2.5:3b\n"
            "В .env:\n"
            "  LLM_PROVIDER=ollama\n"
            "Затем: ./scripts/start-ollama.sh\n"
            f"\nОшибка: {e}"
        ) from e

    print("ping:", json.dumps(info, ensure_ascii=False))
    if provider_name() != "ollama":
        print(
            "WARNING: сейчас не Ollama. Поставь в .env:\n"
            "  LLM_PROVIDER=ollama"
        )

    note = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Завтра созвон с инвесторами"
    result = categorize_note(note)
    print(f"IN:  {note}")
    print(f"OUT: {format_result(result)}")
    print(f"JSON: {json.dumps(result.model_dump(mode='json'), ensure_ascii=False)}")


if __name__ == "__main__":
    main()
