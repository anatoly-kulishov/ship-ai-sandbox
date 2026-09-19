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
  *)
    echo "Usage: ./run.sh [hub|01|02]"
    exit 1
    ;;
esac
