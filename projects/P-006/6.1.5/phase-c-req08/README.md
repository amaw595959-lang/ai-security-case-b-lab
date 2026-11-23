# P-006 Phase C — REQ-08 native event, audit and retention checks

The original experiment compared native content-bearing receipts with a metadata-only local capture. Its dispatcher replacement skipped the native sink chain even for unrelated events. The corrected lab applies an explicit scope to a single synthetic notice operation and leaves unrelated dispatch and audit on the native path. [Original design](design.md) · [Original report](report.md) · [Defect analysis](defect-analysis.md) · [Event security policy](event-security-policy.md) · [Retest](retest.md)

| File | Responsibility |
| --- | --- |
| [Notice policy](overlay/capture.py) | Binds an admitted request to its actor, records only fixed metadata, reports rejected delivery and schedules owner-checked logical expiry. |
| [Pinned source patch](overlay/notice-events.patch) | Checks scope at publication and just before direct inbox consumption. Native dispatch and inbox functions remain in place. |
| [Launcher](run_lab.sh) and [app adapter](overlay/serve_c.py) | Compare source and image bytes, run with read-only source mounts and enable the approved fixture-only entry point. |
| [Runtime check](overlay/check_c.py) and [native observer](tests/native_observer.py) | Send the approved synthetic requests and independently inspect HTTP, the local journals and SQLite. |
| [Offline regressions](tests/test_capture.py) and [pinned dispatcher probe](tests/probe_dispatch.py) | Exercise normal and denied publication, bad or duplicate events, failure records and consumer behavior. The probe uses injected observers for the session and inbox call boundaries. |
| [Historical replay](verify.py) and [original evidence](evidence/SHA256SUMS) | Preserve the first experiment and its original receipts. [Historical implementation snapshot](https://github.com/amaw595959-lang/ai-security-case-b-lab/tree/949cde98871379051ae8cf0af6ed8bd9aa75eaca/projects/P-006/6.1.5/phase-c-req08) |

## Run the offline checks

From the repository root, use Python 3.12. The component tests use the standard library. The archive replay checks the original comparison and controlled ledgers.

~~~bash
phase=projects/P-006/6.1.5/phase-c-req08
python3.12 -B -m unittest discover -s "$phase/tests" -v
(cd "$phase/evidence" && sha256sum --strict -c SHA256SUMS)
python3.12 -B "$phase/verify.py"
(cd "$phase/evidence/retest" && sha256sum --strict -c SHA256SUMS)
~~~

## Reproduce the isolated retest

Use Linux amd64 Docker and Python 3.12. Pull the pinned Open WebUI and llama.cpp images and verify the public model artifact using the linked Phase B preparation. The launcher expects the directory containing `model.gguf`, a fresh output directory, and a checkout of the pinned Open WebUI source. [Image and model preparation](../../6.1.4/phase-b-req07/README.md#reproduce)

~~~bash
phase=projects/P-006/6.1.5/phase-c-req08
umask 077
work=$(mktemp -d /tmp/p006-req08.XXXXXX)
git clone --depth 1 --branch v0.13.4 https://github.com/open-webui/open-webui.git "$work/upstream"
test "$(git -C "$work/upstream" rev-parse HEAD)" = 0666e59d26a4d056e0bacee41742486badd71cf8
python3.12 -B projects/P-006/6.1.1/model-evaluation/fetch_model.py "$work/model"
chmod 0755 "$work"
set -o pipefail
bash "$phase/run_lab.sh" "$work/model" "$work/observed" "$work/upstream" 2>&1 | tee "$work/execution.txt"
~~~

The launcher runs the pinned dispatcher probe without network, then starts fresh Open WebUI and model containers that share a loopback-only namespace. They use synthetic accounts, no published ports and temporary stores. The output directory includes private logs for diagnosis. The archived review evidence uses the separate sanitized observations. Observe the known native and scoped deliveries first. Then inspect the tests for absence of restricted content and compare the owner and unrelated-user responses with SQLite. [Acceptance rules](event-security-policy.md#acceptance) · [Executed commands and results](retest.md)

## Reproduce

For the before-change comparison, check out the historical implementation into a fresh read-only snapshot. Its deliberately content-bearing test copies are synthetic and belong in the private exercise directory. Use the original launcher at its pinned revision. [Original instructions](https://github.com/amaw595959-lang/ai-security-case-b-lab/blob/949cde98871379051ae8cf0af6ed8bd9aa75eaca/projects/P-006/6.1.5/phase-c-req08/README.md#reproduce)

With the pinned image loaded, run the current probe against the native runtime and the old overlay. Set `legacy_overlay` to the original snapshot's `overlay` directory. The probe must be readable by the isolated container.

~~~bash
phase=projects/P-006/6.1.5/phase-c-req08
image=ghcr.io/open-webui/open-webui@sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1
for mode in native legacy; do
  run_id=$(python3.12 -B -c 'from uuid import uuid4; print(uuid4())')
  docker run --rm --pull never --network none --cap-drop ALL --security-opt no-new-privileges \
    --env-file projects/P-006/6.1.4/phase-b-req07/lab.env \
    -e PYTHONPATH=/app/backend -e ENABLE_FUNCTIONS=false -e GLOBAL_LOG_LEVEL=WARNING \
    -e P006_DATA_MODE=controlled -e "P006_RUN_ID=$run_id" \
    --mount "type=bind,src=$(realpath "$phase/tests/probe_dispatch.py"),dst=/probe_dispatch.py,readonly" \
    --mount "type=bind,src=$legacy_overlay,dst=/p006-legacy,readonly" \
    --tmpfs /p006-state:rw,noexec,nosuid,nodev,mode=0700 \
    "$image" python3 -B /probe_dispatch.py "$mode"
done
~~~
