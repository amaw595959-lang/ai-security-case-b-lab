# P-006 Phase B — Open WebUI REQ-07

An in-process preview extension for the pinned Open WebUI release. The design defines the authorized topology, scoped identities, state transitions and expected cases. [Integration design](design.md)

The executed application checks, limitations and independent observations are recorded in the report. [Phase B report](report.md)

| File | Purpose |
| --- | --- |
| `overlay/serve.py` | Creates the temporary data directory and session key, loads the native Open WebUI app, and adds the lab routes before the frontend fallback. |
| `overlay/preview.py` | Checks native sessions, exact private chat ownership, notice revision and assigned reviewer. Builds the preview from the approved fields. |
| `overlay/check_http.py` | Executes the genuine loopback API workflow and reads the two SQLite databases through separate, read-only connections. Records case and operation IDs and redacts authentication inputs and outputs. |
| `lab.env` | Sets the local model route and lab feature switches. The file contains no secret. |
| `start.sh` | Validates the image source revision and starts the two local containers. The model owns an isolated network namespace that the application shares. |

## Reproduce

Use a local Linux amd64 Docker engine and host Python 3.12. The local names `p006-req07-model` and `p006-req07-webui` must be available. The scripts refuse an existing name. From the repository root run the following. The public downloads are the pinned images and model. Both applications communicate inside the shared loopback namespace.

```bash
cd projects/P-006/6.1.4/phase-b-req07
p006_work=$(mktemp -d /tmp/p006-phase-b.XXXXXX)
docker pull --platform linux/amd64 ghcr.io/open-webui/open-webui@sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1
docker pull --platform linux/amd64 ghcr.io/ggml-org/llama.cpp@sha256:c2cf6c72d913b6c89a5f0929f2a866e6161e09e7dc187e0f3b0f21e923e26db3
python3.12 -B ../../6.1.1/model-evaluation/fetch_model.py "$p006_work/model"
chmod 0755 overlay
chmod 0644 overlay/*.py
bash start.sh "$p006_work/model"
docker exec -i p006-req07-webui python3 -B /p006/check_http.py \
  < ../../6.1.1/practice-lab/fixtures/case-b.json > "$p006_work/http.jsonl"
```

The public overlay files must be readable by the container's mapped user. Their mount is read-only. The launcher uses a temporary private state directory, and the check creates its synthetic accounts in that new instance. It registers the pinned model and grants the analyst native read access. The standard analyst and reviewer only exercise their ordinary user sessions. The test creates the saved candidate and records the completion, then queries the private chat and gate state independently.

Inspect the request and reply, separate SQLite observations, model and identity records, and coverage decisions in the resulting JSON lines. Preserve the run directory if a check fails. A fresh repeat needs new containers and synthetic credentials.

After recording the evidence from this exercise, remove its containers and temporary in-container state.

```bash
docker stop --timeout 5 p006-req07-webui p006-req07-model
docker rm p006-req07-webui p006-req07-model
```
