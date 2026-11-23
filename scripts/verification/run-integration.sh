#!/usr/bin/env bash
set -euo pipefail
if [[ "$#" != 2 || "$1" != --confirm-isolated ]]; then
  printf 'Use --confirm-isolated and provide a new private output directory.\n' >&2
  exit 2
fi

root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
umask 077
mkdir -- "$2"
work=$(realpath "$2")
cd "$root"
base=projects/P-006
phase_b=$base/6.1.4/phase-b-req07
phase_c=$base/6.1.5/phase-c-req08
fixture=$base/6.1.1/practice-lab/fixtures/case-b.json
app=ghcr.io/open-webui/open-webui@sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1
model=ghcr.io/ggml-org/llama.cpp@sha256:c2cf6c72d913b6c89a5f0929f2a866e6161e09e7dc187e0f3b0f21e923e26db3
setup=BLOCKED
b_result=NOT_TESTED
c_result=NOT_TESTED
b_exit=
c_exit=
owns_b=false

clean_b() {
  local name container
  if [[ "$owns_b" == true && -f "$work/phase-b-start.log" ]]; then
    while IFS= read -r container; do
      if [[ ! "$container" =~ ^[0-9a-f]{64}$ ]]; then continue; fi
      name=$(docker container inspect --format '{{.Name}}' "$container" 2>/dev/null || true)
      if [[ "$name" == /p006-req07-webui || "$name" == /p006-req07-model ]]; then
        docker rm -f "$container" >> "$work/cleanup.log" 2>&1 || true
      fi
    done < "$work/phase-b-start.log"
    owns_b=false
  fi
}

completed_suite() {
  python3.12 -B - "$1" <<'PY'
import json
import sys
from pathlib import Path
from uuid import UUID

try:
    rows = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line]
    uuid = str(UUID(rows[0]["run_id"]))
    observed = all(row["run_id"] == uuid for row in rows)
    complete = rows[-1]["event"] == "suite" and rows[-1]["status"] == "PASS"
except (OSError, ValueError, IndexError, KeyError, TypeError):
    sys.exit(1)
sys.exit(0 if observed and complete else 1)
PY
}

finish() {
  local code=$?
  clean_b
  python3.12 -B - "$work" "$code" "$setup" "$b_result" "$c_result" "$b_exit" "$c_exit" <<'PY'
import json
import os
import sys
from pathlib import Path
from uuid import UUID

root = Path(sys.argv[1])
code = int(sys.argv[2])
setup, b_result, c_result = sys.argv[3:6]

def read_id(filename):
    path = root / filename
    if not path.is_file() or not path.stat().st_size:
        return None
    try:
        first = json.loads(path.read_text().splitlines()[0])
        return str(UUID(first["run_id"]))
    except (OSError, ValueError, KeyError, TypeError):
        return None

rid = os.environ.get("GITHUB_RUN_ID", "")
summary = {
    "schema_version": 1,
    "scope": "isolated integration",
    "status": "PASS" if code == 0 else "BLOCKED" if code == 2 else "FAIL",
    "exit_code": code,
    "github_run_id": rid if rid.isdecimal() else None,
    "preparation": setup,
    "req07": {"status": b_result, "run_id": read_id("phase-b.jsonl"), "exit_code": int(sys.argv[6]) if sys.argv[6] else None},
    "req08": {"status": c_result, "run_id": read_id("phase-c/results.jsonl"), "exit_code": int(sys.argv[7]) if sys.argv[7] else None},
}
destination = root / "integration.json"
destination.write_text(json.dumps(summary, indent=2) + "\n")
print(destination.read_text(), end="")
PY
}
trap finish EXIT

if [[ "$(uname -s)/$(uname -m)" != Linux/x86_64 ]] || ! docker info > "$work/docker-info.log" 2>&1; then
  printf 'BLOCKED. The isolated Linux amd64 Docker prerequisite is unavailable.\n'
  exit 2
fi
# Keep model artifacts private. Public user-mode mount files are readable on the fresh runner.
chmod 0755 "$work"
if ! {
  docker pull --platform linux/amd64 "$app" &&
  docker pull --platform linux/amd64 "$model" &&
  git clone --depth 1 --branch v0.13.4 --single-branch https://github.com/open-webui/open-webui.git "$work/upstream" &&
  python3.12 -B "$base/6.1.1/model-evaluation/fetch_model.py" "$work/model"
} > "$work/setup.log" 2>&1; then
  printf 'BLOCKED. An image, source or model preparation command failed.\n'
  exit 2
fi
pin=0666e59d26a4d056e0bacee41742486badd71cf8
image_revision=$(docker image inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' "$app")
if [[ "$(git -C "$work/upstream" rev-parse HEAD)" != "$pin" || "$image_revision" != "$pin" ]]; then
  setup=FAIL
  printf 'FAIL. Upstream tag or image label differs from the approved source commit.\n'
  exit 1
fi
setup=PASS

reserved=false
for container in p006-req07-webui p006-req07-model; do
  if docker container inspect "$container" >/dev/null 2>&1; then reserved=true; fi
done
if [[ "$reserved" == true ]]; then
  b_result=BLOCKED
  printf 'REQ-07 BLOCKED. Fresh container names are unavailable.\n'
else
  owns_b=true
  b_exit=0
  if bash "$phase_b/start.sh" "$work/model" > "$work/phase-b-start.log" 2>&1; then
    docker exec p006-req07-webui python3.12 -B -c \
      'import socket; assert [name for _, name in socket.if_nameindex()] == ["lo"]' \
      >> "$work/phase-b-start.log" 2>&1 || b_exit=$?
    if [[ "$b_exit" == 0 ]]; then
      docker exec -i p006-req07-webui python3.12 -B /p006/check_http.py < "$fixture" \
        > "$work/phase-b.jsonl" 2> "$work/phase-b-errors.log" || b_exit=$?
    fi
    if [[ "$b_exit" == 0 ]] && completed_suite "$work/phase-b.jsonl"; then
      b_result=PASS
    else
      b_result=FAIL
    fi
  else
    b_exit=$?
    b_result=BLOCKED
  fi
  clean_b
fi

c_exit=0
bash "$phase_c/run_lab.sh" "$work/model" "$work/phase-c" "$work/upstream" \
  > "$work/phase-c-execution.log" 2>&1 || c_exit=$?
case "$c_exit" in
  0)
    if completed_suite "$work/phase-c/results.jsonl"; then c_result=PASS; else c_result=FAIL; fi
    ;;
  2) c_result=BLOCKED ;;
  *) c_result=FAIL ;;
esac

if [[ "$b_result" == FAIL || "$c_result" == FAIL ]]; then exit 1; fi
if [[ "$b_result" != PASS || "$c_result" != PASS ]]; then exit 2; fi
