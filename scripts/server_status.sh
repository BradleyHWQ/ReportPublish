#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.server"
PID_FILE="$STATE_DIR/http.server.pid"
META_FILE="$STATE_DIR/http.server.meta"

resolve_server_pid() {
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

  rm -f "$PID_FILE" "$META_FILE"
  return 1
}

SERVER_PID="$(resolve_server_pid || true)"

if [[ -z "$SERVER_PID" ]]; then
  echo "Server is not running"
  exit 1
fi

echo "Server is running"
if [[ -f "$META_FILE" ]]; then
  cat "$META_FILE"
else
  echo "PID=$SERVER_PID"
fi
