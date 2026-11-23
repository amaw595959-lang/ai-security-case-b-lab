#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
umask 077
artifact_dir=$(realpath "$1")
output_dir=$(realpath "$2")
upstream=$(realpath "$3")
source_commit=0666e59d26a4d056e0bacee41742486badd71cf8
app_image=ghcr.io/open-webui/open-webui@sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1
phase_b=$(realpath ../../6.1.4/phase-b-req07)
fixture=$(realpath ../../6.1.1/practice-lab/fixtures/case-b.json)
mkdir "$output_dir"
test "$(git -C "$upstream" rev-parse HEAD)" = "$source_commit"
test "$(docker image inspect --format '{{.Os}}/{{.Architecture}} {{index .Config.Labels "org.opencontainers.image.revision"}}' "$app_image")" = "linux/amd64 $source_commit"
run_id=$(python3.12 -B -c 'from uuid import uuid4; print(uuid4())')
app_name=p006-req08-app-${run_id:0:8}
model_name=p006-req08-model-${run_id:0:8}
scratch=$(mktemp -d /tmp/p006-req08-runtime.XXXXXX)
chmod 0755 "$scratch"
mkdir -m 0755 "$scratch/overlay" "$scratch/phase-b" "$scratch/tests"
cleanup() {
  for name in "$app_name" "$model_name"; do
    if docker container inspect "$name" >/dev/null 2>&1; then
      docker rm -f "$name" >/dev/null
    fi
  done
}
trap cleanup EXIT
for name in "$app_name" "$model_name"; do
  if docker container inspect "$name" >/dev/null 2>&1; then
    trap - EXIT
    printf 'Out-of-scope existing container name: %s\n' "$name" >&2
    exit 1
  fi
done
install -m 0644 overlay/*.py "$scratch/overlay"
install -m 0644 "$phase_b"/overlay/*.py "$scratch/phase-b"
install -m 0644 tests/{native_observer,probe_dispatch}.py "$scratch/tests"
install -m 0644 "$fixture" "$scratch/fixture.json"
modules=(backend/open_webui/events.py backend/open_webui/utils/middleware.py)
for module in "${modules[@]}"; do
  mkdir -p -m 0755 "$scratch/source/$(dirname "$module")"
  git -C "$upstream" show "$source_commit:$module" > "$scratch/source/$module"
  read -r source_hash _ < <(sha256sum "$scratch/source/$module")
  image_hash=$(docker run --rm --pull never --network none --cap-drop ALL --security-opt no-new-privileges \
    "$app_image" sha256sum "/app/$module" | cut -d ' ' -f 1)
  test "$source_hash" = "$image_hash"
  printf 'Original source and image hash %s %s\n' "$module" "$source_hash"
done
patch=$(realpath overlay/notice-events.patch)
(cd "$scratch/source" && git apply --check "$patch" && git apply "$patch")
mounts=()
for module in "${modules[@]}"; do
  chmod 0644 "$scratch/source/$module"
  mounts+=(--mount "type=bind,src=$scratch/source/$module,dst=/app/$module,readonly")
done

printf 'REQ-08 retest run %s\n' "$run_id"
probe_status=0
docker run --rm --pull never --network none --cap-drop ALL --security-opt no-new-privileges \
  --env-file "$phase_b/lab.env" -e PYTHONPATH=/app/backend:/p006-c \
  -e ENABLE_FUNCTIONS=false -e GLOBAL_LOG_LEVEL=WARNING -e "P006_RUN_ID=$run_id" \
  --mount "type=bind,src=$scratch/overlay,dst=/p006-c,readonly" \
  --mount "type=bind,src=$scratch/tests,dst=/p006-tests,readonly" \
  "${mounts[@]}" --tmpfs /p006-state:rw,noexec,nosuid,nodev,mode=0700 \
  "$app_image" python3 -B /p006-tests/probe_dispatch.py fixed \
  > "$output_dir/private-dispatch.log" 2>&1 || probe_status=$?
printf 'Pinned dispatch probe exit code %s\n' "$probe_status"
if [[ "$probe_status" != 0 ]]; then
  exit "$probe_status"
fi
python3.12 -B - "$output_dir/private-dispatch.log" <<'PY' | tee "$output_dir/dispatch-probe.txt"
import json
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text()
assert "fictional restricted notice sentinel" not in raw
assert "synthetic native test sink unavailable" in raw
records = [json.loads(line) for line in raw.splitlines() if line.startswith("{")]
assert len(records) == 2 and all(record["mode"] == "fixed" for record in records)
for record in records:
    print(json.dumps(record, sort_keys=True))
print("Injected native consumer failure observed. Restricted sentinel count 0.")
PY

python3.12 -B - "$artifact_dir" "$model_name" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path("../../6.1.1/model-evaluation").resolve()))
import evaluate

evaluate.PLAN = {**evaluate.PLAN, "container": sys.argv[2]}
evaluate.start_lab(Path(sys.argv[1]))
PY
docker run --name "$app_name" --detach --pull never \
  --label caseb.lab=P006-CASEB-LAB-01-C-RETEST --network "container:$model_name" \
  --cap-drop ALL --security-opt no-new-privileges --env-file "$phase_b/lab.env" \
  -e PYTHONPATH=/app/backend:/p006-b:/p006-c:/p006-tests -e GLOBAL_LOG_LEVEL=WARNING \
  -e "P006_RUN_ID=$run_id" -e P006_OBSERVE_NATIVE=1 -e ENABLE_FUNCTIONS=false \
  -e AUDIT_LOG_LEVEL=METADATA -e AUDIT_INCLUDED_PATHS= -e 'AUDIT_EXCLUDED_PATHS=p006/notice/chat$' \
  -e ENABLE_AUDIT_LOGS_FILE=true -e ENABLE_AUDIT_STDOUT=false \
  -e AUDIT_LOGS_FILE_PATH=/p006-state/native-audit.jsonl \
  --mount "type=bind,src=$scratch/phase-b,dst=/p006-b,readonly" \
  --mount "type=bind,src=$scratch/overlay,dst=/p006-c,readonly" \
  --mount "type=bind,src=$scratch/tests,dst=/p006-tests,readonly" \
  --mount "type=bind,src=$scratch/fixture.json,dst=/p006-fixture.json,readonly" \
  "${mounts[@]}" --tmpfs /p006-state:rw,noexec,nosuid,nodev,mode=0700 \
  "$app_image" python3 -B /p006-c/serve_c.py

status=2
for (( step=0; step < 60; step++ )); do
  if docker exec "$app_name" curl -q --noproxy 127.0.0.1 -fsS --max-time 3 http://127.0.0.1:3000/api/version 2>/dev/null; then
    printf '\n'
    status=0
    break
  fi
  if [[ "$(docker container inspect --format '{{.State.Running}}' "$app_name")" != true ]]; then
    break
  fi
  sleep 1
done
if [[ "$status" = 0 ]]; then
  {
    docker inspect "$model_name" "$app_name" --format '{{.Name}} {{.Image}} {{.HostConfig.NetworkMode}} {{json .HostConfig.PortBindings}}'
    docker exec "$app_name" python3 -B -c 'import socket; assert [name for _, name in socket.if_nameindex()] == ["lo"]; print("interfaces: lo")'
    docker exec "$model_name" sha256sum /models/model.gguf
    docker exec "$model_name" /app/llama-server --version
    docker exec "$app_name" sha256sum /app/backend/open_webui/main.py /app/backend/open_webui/events.py /app/backend/open_webui/utils/middleware.py
  } > "$output_dir/topology.txt" 2>&1
  docker exec -i "$app_name" python3 -B /p006-c/check_c.py < "$fixture" \
    > "$output_dir/results.jsonl" 2> "$output_dir/check-errors.txt" || status=$?
fi
docker logs "$app_name" > "$output_dir/private-app.log" 2>&1
if [[ "$status" = 0 ]]; then
  python3.12 -B - "$output_dir/private-app.log" <<'PY' | tee "$output_dir/log-observation.txt" || status=$?
import hashlib
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_bytes()
markers = (b"LAB-INT-042", b"Maple Calendar", b"content_preview")
counts = [raw.count(marker) for marker in markers]
print(f"Application console SHA-256 {hashlib.sha256(raw).hexdigest()}")
print(f"Assessed restricted-content marker counts {counts}")
assert counts == [0, 0, 0]
PY
fi
printf 'REQ-08 retest run %s exit code %s\n' "$run_id" "$status"
exit "$status"
