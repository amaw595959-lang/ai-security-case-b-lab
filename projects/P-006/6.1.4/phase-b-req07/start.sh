#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
app_image=ghcr.io/open-webui/open-webui@sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1
source_commit=0666e59d26a4d056e0bacee41742486badd71cf8
revision=$(docker image inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' "$app_image")
test "$revision" = "$source_commit"
for local_name in p006-req07-model p006-req07-webui; do
  if docker container inspect "$local_name" >/dev/null 2>&1; then
    printf 'Container name already exists: %s\n' "$local_name" >&2
    exit 1
  fi
done
python3.12 -B - "$1" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('../../6.1.1/model-evaluation').resolve()))
import evaluate
evaluate.PLAN = {**evaluate.PLAN, 'container': 'p006-req07-model'}
evaluate.start_lab(Path(sys.argv[1]))
PY
docker run --name p006-req07-webui --detach --pull never \
  --label caseb.lab=P006-CASEB-LAB-01-B --network container:p006-req07-model \
  --cap-drop ALL --security-opt no-new-privileges --env-file lab.env \
  --mount "type=bind,src=$PWD/overlay,dst=/p006,readonly" \
  --tmpfs /p006-state:rw,noexec,nosuid,nodev,mode=0700 \
  "$app_image" python3 -B /p006/serve.py
for (( step = 0; step < 60; step++ )); do
  if docker exec p006-req07-webui curl -q --noproxy 127.0.0.1 -fsS \
    --max-time 3 http://127.0.0.1:3000/api/version 2>/dev/null; then
    printf '\n'
    exit 0
  fi
  test "$(docker container inspect --format '{{.State.Running}}' p006-req07-webui)" = true
  sleep 1
done
printf '%s\n' 'Open WebUI did not become ready.' >&2
exit 1
