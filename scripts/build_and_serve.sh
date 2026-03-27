#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
SHOW_CODE=false

POSITIONAL_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --show-code)
      SHOW_CODE=true
      ;;
    *)
      POSITIONAL_ARGS+=("$arg")
      ;;
  esac
done

if [[ ${#POSITIONAL_ARGS[@]} -ge 1 ]]; then
  PORT="${POSITIONAL_ARGS[0]}"
fi

if [[ ${#POSITIONAL_ARGS[@]} -ge 2 ]]; then
  HOST="${POSITIONAL_ARGS[1]}"
fi

cd "$ROOT_DIR"
if [[ "$SHOW_CODE" == "true" ]]; then
  python3 scripts/publish.py --show-code ${PUBLISH_ARGS:-}
else
  python3 scripts/publish.py ${PUBLISH_ARGS:-}
fi

echo "Serving _build/html at http://${HOST}:${PORT}"
exec python3 -m http.server "$PORT" --bind "$HOST" --directory "$ROOT_DIR/_build/html"
