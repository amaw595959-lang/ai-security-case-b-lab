# P-006 Phase C — Native event, audit and retention verification

This phase exercises the pinned Open WebUI application with the scoped REQ-08 policy. The branch builds on Phase B to reuse the native app launcher, role provisioning and SQL evidence helpers. The design specifies the observed boundaries, experiment and permitted copies. [Data-handling design](design.md)

The assessment report links the executed comparison, scope limits and independent verification commands. [Phase C report](report.md)

| File | Responsibility |
| --- | --- |
| `overlay/capture.py` | Projects native events before operational dispatch. It keeps approved HTTP decision metadata, suppresses the unapproved inbox path, and schedules expiry for the exact verified owner's chat. |
| `overlay/serve_c.py` | Installs the scoped policy in the actual Open WebUI process before its main module loads. |
| `overlay/check_c.py` | Exercises ordinary native chat, reads the journals and SQLite from an independent process, and validates the allowed and excluded data. |
| `run_lab.sh` | Runs two fresh app containers against one pinned local model and captures their outcomes and topology. It removes the exercise's containers at exit. |

## Reproduce

Use a local Linux amd64 Docker engine and host Python 3.12. Download the pinned images and verified GGUF as in the Phase B instructions. The C harness expects the directory containing the GGUF named `model.gguf` and a new output path inside a private temporary directory. [Artifact setup](../../6.1.4/phase-b-req07/README.md#reproduce)

```bash
cd projects/P-006/6.1.5/phase-c-req08
umask 077
p006_work=$(mktemp -d /tmp/p006-phase-c.XXXXXX)
python3.12 -B ../../6.1.1/model-evaluation/fetch_model.py "$p006_work/model"
chmod 0755 overlay ../../6.1.4/phase-b-req07/overlay
chmod 0644 overlay/*.py ../../6.1.4/phase-b-req07/overlay/*.py
set -o pipefail
bash run_lab.sh "$p006_work/model" "$p006_work/observed" 2>&1 | tee "$p006_work/execution.txt"
```

The readable files contain public exercise source. Their mounts are read-only. Each mode uses temporary state, only loopback and newly generated synthetic identities. The comparison deliberately enables native body auditing with fictional data. Keep its raw state inside the lab and publish only the necessary synthetic chat receipts. The controlled run uses native auditing `NONE`, an explicit metadata-only journal for the assessed HTTP decision, and a 12-second chat expiry. It waits up to 25 seconds to observe the actual state, then queries the same chat through the native route.

Compare both execution logs and JSON ledgers. For the input preview and completion path, start with the native source receipts in baseline and both successful deliveries in controlled. For audit, check that the request and response were observed before the change and that the controlled HTTP decision actually arrived. For retention, confirm the owner could read, the unrelated user was denied, and the chat and message rows expired. [T04 acceptance evidence](../../6.1.1/case-b-test-design.md#p006-611-t04--proposed-req-08-storage-event-and-log-handling)
