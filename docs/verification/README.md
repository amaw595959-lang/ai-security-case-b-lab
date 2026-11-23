# P-006 engineering verification

The fast suite checks the Git working tree, frozen evidence and deterministic security tests. The manual suite exercises the authorized synthetic Open WebUI deployment. Each suite reports its own result. The historical standalone-model and integration verdicts retain their original scope. [Current-status index](status.md) · [6.1.1 design closure](../../projects/P-006/6.1.1/closure-report.md)

## Run locally

Use a Linux x86-64 Git checkout and CPython 3.12. The lock identifies the exact Python wheels for this platform. The installation commands need access to the public package and release servers. The offline verification command itself uses the working tree, locally available Git objects and the installed tools.

~~~bash
p006_verify_work=$(mktemp -d /tmp/p006-verification.XXXXXX)
python3.12 -m venv "$p006_verify_work/venv"
"$p006_verify_work/venv/bin/python" -m pip install --disable-pip-version-check \
  --require-hashes --only-binary=:all: -r scripts/verification/requirements.lock
bash scripts/verification/install-actionlint.sh "$p006_verify_work/bin"
"$p006_verify_work/venv/bin/python" -B scripts/verification/verify.py \
  --actionlint "$p006_verify_work/bin/actionlint" \
  --json "$p006_verify_work/offline.json"
~~~

Git must have the commit objects used by pinned links. The checkout action retrieves Git history. If an old Phase C commit is missing from your local clone, fetch the original pinned object and repeat the check.

~~~bash
git fetch --no-tags https://github.com/amaw595959-lang/ai-security-case-b-lab.git \
  949cde98871379051ae8cf0af6ed8bd9aa75eaca
~~~

To verify the source lock against actual Open WebUI blobs, obtain a local source checkout at `0666e59d26a4d056e0bacee41742486badd71cf8`. Use its path with the same verifier.

~~~bash
git clone --depth 1 --branch v0.13.4 https://github.com/open-webui/open-webui.git \
  "$p006_verify_work/open-webui"
"$p006_verify_work/venv/bin/python" -B scripts/verification/verify.py \
  --upstream "$p006_verify_work/open-webui" \
  --actionlint "$p006_verify_work/bin/actionlint" \
  --json "$p006_verify_work/with-source.json"
~~~

The JSON summary lists the Git revision, scope, check statuses, known counts and process exit codes. Exit `0` means the required checks in that suite passed, `1` means at least one check failed, and `2` means a required prerequisite was unavailable without a verified failure. Optional checks omitted from the offline invocation are `NOT_TESTED`. A timed-out required command is marked `BLOCKED`. GitHub supplies its run ID to the summary when the job runs. The full diagnostic output from an individual test command can be inspected locally.

## Checks and verification scope

| Check | What the result establishes |
| --- | --- |
| Markdown and source citations | CommonMark links and images, table and reference links, filename case and heading anchors resolve within the repository. Pinned GitHub links to this repository require local commit objects. Open WebUI permalinks must use the pin and the paths and line ranges in the source lock. Pass `--upstream` to check the locked bytes and line counts directly. General external URLs are counted as unchecked. [Reference checker](../../scripts/verification/references.py) · [Source lock](../../scripts/verification/source-lock.json) |
| Canonical IDs and traceability | The 110 risk and 334 work-package IDs, P-006 title and work-package mapping, 14 study rows, nine requirements, seven invariants, eight boundaries and four test IDs must agree. Forward and reverse mappings are compared against the documented source, and each requirement needs an evidence or coverage-gap entry and accountable role. [Catalog checker](../../scripts/verification/catalog.py) |
| Archive integrity and replay | Recalculate all known SHA-256 manifest entries, check the six practice-transcript hashes separately, and reject missing or changed frozen manifests. The REQ-07 standalone manifest resolves its paths from the demo directory. Retest manifests may reference code in parent directories inside the repository. New experiments can add new manifests. Replay the saved model, HTTP, SQLite and event records against their bounded oracles. [Archive checker](../../scripts/verification/archives.py) |
| Offline execution | Re-run the original practice fixtures, the standalone HTTP/SQLite REQ-07 demonstration, the REQ-08 event-policy tests and the verifier tests. These runs use fixtures and loopback components. Python compilation, Ruff correctness rules, Bash syntax and actionlint checks run separately. [Suite runner](../../scripts/verification/verify.py) |
| Sanitization | Scan repository text and compressed evidence, check high-confidence secret patterns and credential fields, and require fixture email domains in published evidence. The Phase C replays also check the operational metadata structure and restricted synthetic indicators. Historical raw synthetic inputs remain at their approved evidence levels. File sizes and unsupported binary evidence that prevent scanning are reported. These checks have limited detection coverage. [Sanitization logic](../../scripts/verification/archives.py) |

The first review found three links from earlier 6.1.1 documents to the original checklist heading. A named compatibility anchor in the current 6.1.1 index restores those links. The source documents, closure and micro-task records retain their existing wording. [Checklist](../../projects/P-006/6.1.1/README.md#first-deliverables-not-completed)

## GitHub Actions security

Both workflows grant `contents: read` and use ephemeral GitHub-hosted Linux runners. Checkout clears persisted credentials. The fast workflow uses `pull_request` for candidate code and supplies no repository secrets. It executes archive replays and offline tests only. The optional workflow gates its job on a manual isolation confirmation and the reviewed `main` ref. Repository changes to the workflow and verifier should be reviewed as code. [Fast workflow](../../.github/workflows/verify.yml) · [Manual workflow](../../.github/workflows/integration.yml)

Checkout v4.2.2, setup-python v5.6.0 and upload-artifact v4.6.2 are referenced by their verified Git commit SHAs. Python wheels are pinned with SHA-256, and the actionlint v1.7.7 Linux archive is checked against a recorded release checksum. The verifier checks YAML policy and actionlint checks the GitHub Actions expressions and configuration. Only the bounded JSON summaries are uploaded. Raw HTTP, application diagnostics, SQLite files and confidential prompts stay in the controlled run directory. [Workflow policy checker](../../scripts/verification/workflows.py) · [Dependency lock](../../scripts/verification/requirements.lock) · [actionlint installer](../../scripts/verification/install-actionlint.sh)

## Optional controlled integration

Run this only on a fresh isolated Linux amd64 Docker runner with permission to fetch the public pinned artifacts. On GitHub, the job requires a manual run on `main` after review and an explicit isolation confirmation. For a local run, provide a new directory under a temporary path. Inspect raw records only in the local temporary directory.

~~~bash
p006_integration_work=$(mktemp -d /tmp/p006-integration.XXXXXX)
bash scripts/verification/run-integration.sh --confirm-isolated \
  "$p006_integration_work/observed"
~~~

The runner checks the source and image identity and uses the model artifact verifier. It calls the existing Phase B and corrected Phase C launchers with synthetic fixtures and reads the final suite receipts. Each phase must have a valid run ID and completed record to count as passed. Its JSON distinguishes `NOT_TESTED` phases and `BLOCKED` prerequisites from actual test failures. A GitHub job skipped by the manual gate is shown as skipped in Actions. [Local runner](../../scripts/verification/run-integration.sh) · [Phase B reproduction](../../projects/P-006/6.1.4/phase-b-req07/README.md#reproduce) · [Phase C reproduction](../../projects/P-006/6.1.5/phase-c-req08/README.md#reproduce-the-isolated-retest)
