#!/usr/bin/env bash
# Usage: ./run.sh          → hub
#        ./run.sh 01       → only lesson 01
#        ./run.sh 02       → only lesson 02
set -euo pipefail
cd "$(dirname "$0")"
# shellcheck disable=SC1091
source .venv/bin/activate

case "${1:-hub}" in
  hub|"" ) exec streamlit run app.py --server.port 8501 ;;
  01|1)    exec streamlit run 01-note-sorter/app.py --server.port 8502 ;;
  02|2)    exec streamlit run 02-tool-use/app.py --server.port 8503 ;;
  03|3)    exec streamlit run 03-ollama/app.py --server.port 8504 ;;
  04|4)    exec streamlit run 04-gym-plan/app.py --server.port 8505 ;;
  05|5)    exec streamlit run 05-rag/app.py --server.port 8506 ;;
  06|6)    exec streamlit run 06-gguf/app.py --server.port 8507 ;;
  *)
    echo "Usage: ./run.sh [hub|01|02|03|04|05|06]"
    exit 1
    ;;
esac
