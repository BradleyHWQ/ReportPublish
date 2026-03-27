#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.server"
PID_FILE="$STATE_DIR/http.server.pid"
LOG_FILE="$STATE_DIR/http.server.log"
META_FILE="$STATE_DIR/http.server.meta"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

resolve_running_pid() {
  local candidate=""
  if [[ -f "$PID_FILE" ]]; then
    candidate="$(cat "$PID_FILE")"
  elif [[ -f "$META_FILE" ]]; then
    candidate="$(sed -n 's/^PID=//p' "$META_FILE" | head -n 1)"
  fi

  if [[ -n "$candidate" ]] && kill -0 "$candidate" 2>/dev/null; then
    echo "$candidate" >"$PID_FILE"
    printf '%s\n' "$candidate"
    return 0
  fi

  rm -f "$PID_FILE"
  return 1
}

if [[ $# -ge 1 ]]; then
  PORT="$1"
fi

if [[ $# -ge 2 ]]; then
  HOST="$2"
fi

mkdir -p "$STATE_DIR"

if EXISTING_PID="$(resolve_running_pid)"; then
  echo "Server already running with PID $EXISTING_PID"
  if [[ -f "$META_FILE" ]]; then
    cat "$META_FILE"
  fi
  exit 0
fi

if [[ ! -f "$ROOT_DIR/_build/html/index.html" ]]; then
  echo "_build/html missing, publishing site first"
  python3 "$ROOT_DIR/scripts/publish.py" ${PUBLISH_ARGS:-}
fi

nohup python3 -m http.server "$PORT" --bind "$HOST" --directory "$ROOT_DIR/_build/html" >"$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" >"$PID_FILE"

sleep 1

if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "Failed to start server. Recent log:"
  tail -n 20 "$LOG_FILE" || true
  rm -f "$PID_FILE"
  exit 1
fi

cat >"$META_FILE" <<EOF
PID=$SERVER_PID
HOST=$HOST
PORT=$PORT
ROOT=$ROOT_DIR/_build/html
LOG=$LOG_FILE
URL=http://127.0.0.1:$PORT
EOF

echo "Started static server"
cat "$META_FILE"
