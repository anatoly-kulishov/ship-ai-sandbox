#!/usr/bin/env bash
# Start local Ollama for lesson 03.
# Usage:
#   ./scripts/start-ollama.sh           # start + ensure default model
#   ./scripts/start-ollama.sh qwen2.5:3b
set -euo pipefail

MODEL="${1:-qwen2.5:3b}"

if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama не найден. Установи: brew install ollama"
  exit 1
fi

if curl -sf -m 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Ollama уже запущен (localhost:11434)"
else
  echo "Запускаю Ollama…"
  if command -v brew >/dev/null 2>&1 && brew services list 2>/dev/null | grep -q '^ollama'; then
    brew services start ollama
  else
    # fallback: foreground-friendly background serve
    nohup ollama serve >/tmp/ollama-serve.log 2>&1 &
    echo "PID $!  (лог: /tmp/ollama-serve.log)"
  fi

  for i in $(seq 1 30); do
    if curl -sf -m 1 http://localhost:11434/api/tags >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
fi

if ! curl -sf -m 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Не удалось поднять Ollama на :11434"
  exit 1
fi

if ! ollama list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$MODEL"; then
  echo "Тяну модель $MODEL …"
  ollama pull "$MODEL"
else
  echo "Модель $MODEL уже есть"
fi

echo
echo "OK. Переключи провайдер в .env:"
echo "  LLM_PROVIDER=ollama"
echo "  (ключи GIGACHAT_* и OLLAMA_* уже могут лежать рядом)"
echo
echo "Проверка: python 03-ollama/check.py \"купить хлеб сегодня\""
echo "Стоп:     ./scripts/stop-ollama.sh"
