#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if [[ $# -ge 1 ]]; then
  PORT="$1"
fi

if [[ $# -ge 2 ]]; then
  HOST="$2"
fi

cd "$ROOT_DIR"
python3 scripts/publish.py

echo "Serving _build/html at http://${HOST}:${PORT}"
exec python3 -m http.server "$PORT" --bind "$HOST" --directory "$ROOT_DIR/_build/html"
