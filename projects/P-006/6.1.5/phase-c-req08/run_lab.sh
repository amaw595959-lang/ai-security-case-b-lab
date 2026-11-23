#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
umask 077
artifact_dir=$(realpath "$1")
output_dir=$(realpath "$2")
mkdir "$output_dir"
phase_b=$(realpath ../../6.1.4/phase-b-req07)
app_image=ghcr.io/open-webui/open-webui@sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1
source_commit=0666e59d26a4d056e0bacee41742486badd71cf8
test "$(docker image inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' "$app_image")" = "$source_commit"
for name in p006-req08-model p006-req08-baseline p006-req08-controlled; do
  if docker container inspect "$name" >/dev/null 2>&1; then
    printf 'Container name already exists: %s\n' "$name" >&2
    exit 1
  fi
done
cleanup() {
  for name in p006-req08-controlled p006-req08-baseline p006-req08-model; do
    if docker container inspect "$name" >/dev/null 2>&1; then
      docker stop --timeout 5 "$name"
      docker rm "$name"
    fi
  done
}
trap cleanup EXIT
python3.12 -B - "$artifact_dir" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path('../../6.1.1/model-evaluation').resolve()))
import evaluate
evaluate.PLAN = {**evaluate.PLAN, 'container': 'p006-req08-model'}
evaluate.start_lab(Path(sys.argv[1]))
PY
total_status=0
for mode in baseline controlled; do
  name=p006-req08-$mode
  run_id=$(python3.12 -B -c 'from uuid import uuid4; print(uuid4())')
  audit_level=NONE
  file_audit=false
  if [[ "$mode" = baseline ]]; then
    audit_level=REQUEST_RESPONSE
    file_audit=true
  fi
  docker run --name "$name" --detach --pull never \
    --label caseb.lab=P006-CASEB-LAB-01-C --network container:p006-req08-model \
    --cap-drop ALL --security-opt no-new-privileges --env-file "$phase_b/lab.env" \
    -e PYTHONPATH=/app/backend:/p006-b:/p006-c -e GLOBAL_LOG_LEVEL=WARNING \
    -e "P006_DATA_MODE=$mode" -e "P006_RUN_ID=$run_id" -e "AUDIT_LOG_LEVEL=$audit_level" \
    -e "ENABLE_AUDIT_LOGS_FILE=$file_audit" -e ENABLE_AUDIT_STDOUT=false \
    -e AUDIT_INCLUDED_PATHS=chat/completions -e AUDIT_EXCLUDED_PATHS= -e MAX_BODY_LOG_SIZE=8192 \
    -e AUDIT_LOGS_FILE_PATH=/p006-state/native-audit.jsonl \
    --mount "type=bind,src=$phase_b/overlay,dst=/p006-b,readonly" \
    --mount "type=bind,src=$PWD/overlay,dst=/p006-c,readonly" \
    --tmpfs /p006-state:rw,noexec,nosuid,nodev,mode=0700 \
    "$app_image" python3 -B /p006-c/serve_c.py
  ready=false
  for (( step=0; step < 60; step++ )); do
    if docker exec "$name" curl -q --noproxy 127.0.0.1 -fsS \
      --max-time 3 http://127.0.0.1:3000/api/version 2>/dev/null; then
      printf '\n'
      ready=true
      break
    fi
    if [[ "$(docker container inspect --format '{{.State.Running}}' "$name")" != true ]]; then
      break
    fi
    sleep 1
  done
  if [[ "$ready" = true ]]; then
    {
      docker inspect p006-req08-model "$name" --format '{{.Name}} {{.Image}} {{.HostConfig.NetworkMode}} {{json .HostConfig.PortBindings}}'
      docker exec "$name" python3 -B -c 'import socket; print("interfaces:", socket.if_nameindex())'
      docker exec p006-req08-model sha256sum /models/model.gguf
      docker exec p006-req08-model /app/llama-server --version
    } > "$output_dir/$mode-topology.txt" 2>&1
    status=0
    docker exec -i "$name" python3 -B /p006-c/check_c.py \
      < ../../6.1.1/practice-lab/fixtures/case-b.json \
      > "$output_dir/$mode.jsonl" 2> "$output_dir/$mode-errors.txt" || status=$?
  else
    status=2
  fi
  docker logs "$name" > "$output_dir/$mode-app.log" 2>&1
  if [[ "$mode" = controlled && "$status" = 0 ]]; then
    if grep -Fq 'LAB-INT-042' "$output_dir/$mode-app.log"; then
      printf 'Controlled application log contained the marker.\n'
      status=1
    else
      printf 'Controlled application log marker count: 0\n'
    fi
  fi
  printf '%s run %s exit status: %s\n' "$mode" "$run_id" "$status"
  if (( status != 0 )); then total_status=1; fi
  docker stop --timeout 5 "$name"
  docker rm "$name"
done
exit "$total_status"
