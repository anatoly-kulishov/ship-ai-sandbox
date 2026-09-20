#!/usr/bin/env bash
# Stop local Ollama (frees RAM/CPU).
set -euo pipefail

if command -v brew >/dev/null 2>&1 && brew services list 2>/dev/null | grep -q '^ollama'; then
  brew services stop ollama || true
fi

pkill -f "ollama serve" 2>/dev/null || true
# runner may linger after serve stops
pkill -x ollama 2>/dev/null || true

sleep 1
if curl -sf -m 1 http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Ollama всё ещё отвечает на :11434 — останови вручную (Activity Monitor → ollama)"
  exit 1
fi

echo "Ollama остановлен"
