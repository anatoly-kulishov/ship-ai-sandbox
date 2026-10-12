#!/usr/bin/env bash
# Usage: ./run.sh          → hub
#        ./run.sh 01       → only lesson 01
set -euo pipefail
cd "$(dirname "$0")"
# shellcheck disable=SC1091
source .venv/bin/activate

case "${1:-hub}" in
  hub|"" ) exec python app.py ;;
  01|1)    exec python 01-note-sorter/app.py ;;
  02|2)    exec python 02-tool-use/app.py ;;
  03|3)    exec python 03-ollama/app.py ;;
  04|4)    exec python 04-gym-plan/app.py ;;
  05|5)    exec python 05-rag/app.py ;;
  06|6)    exec python 06-gguf/app.py ;;
  07|7)    exec uvicorn --app-dir 07-fastapi server:app --port 8600 --reload ;;
  08|8)    exec uvicorn --app-dir 08-asyncio server:app --port 8601 --reload ;;
  *)
    echo "Usage: ./run.sh [hub|01|02|03|04|05|06|07|08]"
    exit 1
    ;;
esac
