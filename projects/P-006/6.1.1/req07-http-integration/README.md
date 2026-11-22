# P-006 / 6.1.1 — Isolated REQ-07 HTTP enforcement demonstration

**Lab:** `P006-CASEB-LAB-01`  
**Deliverable:** a small working application that enforces the proposed `P006-611-REQ-07` preview rule at an **HTTP and SQLite** boundary, with independently observable state.  
**Scope:** local synthetic service-notice workflow only. **This is not an Open WebUI deployment, plugin, patch, or integration test.**

The earlier standalone model run found **B-04 `FAIL`** and **B-05 `FAIL`** for its pinned SmolLM2 artifact, prompts and settings ([recorded results](../model-evaluation/results.md)). This demo uses fixed synthetic drafts, including a wrong time and `LAB-INT-042`, to test *containment*, not real model behavior. The proposed preview gate did not exist in the pinned Open WebUI code under review. Its **Open WebUI integration remains `NOT_TESTED`**. The separate REQ-08 logging, event, and retention integration also remains `NOT_TESTED`.

## What is implemented

| File | Purpose |
| --- | --- |
| [`app.py`](app.py) | Standard-library HTTP server, in-process bearer-token identity registry, enforced analyst/reviewer roles, SQLite notice/approval/ready state, and template-only preview decision |
| [`tests/test_http_preview.py`](tests/test_http_preview.py) | Real loopback HTTP requests, separate SQLite queries and 20 security-focused integration tests; checks T03 A–F plus role/ownership, stale revisions, content handling, no publishing endpoint |
| [`demo_receipts.py`](demo_receipts.py) | Executes T03 A–F over HTTP with separate SQLite reads and creates machine-readable genuine receipts without tokens |
| [`evidence/http-sqlite-receipts.json`](evidence/http-sqlite-receipts.json) | Recorded HTTP status, preview decision, independent DB state and assertions for each of the six variants |
| [`evidence/unittest-output.txt`](evidence/unittest-output.txt) | Two real unittest runs, including an isolated virtual-environment rerun, environment and exit-code evidence |
| [`evidence/SHA256SUMS`](evidence/SHA256SUMS) | SHA-256 fingerprints of the source, tests and recorded receipts |

The application creates three synthetic identities at startup: an analyst, a separate reviewer and an unrelated analyst. Bearer tokens are random values issued **in memory for the test process**. The caller identity and role are resolved server-side, not accepted from a JSON field. Approval of employee facts requires a reviewer credential; audience confirmation and requesting a preview require the notice owner. Each notice is stored in SQLite with its revision and approval. An approval or confirmation for the wrong revision/audience does not make the notice ready. Revision changes clear ready state and approvals.

The server renders employee-ready text only from the reviewer-approved `service_name`, `maintenance_window` and `employee_action` fields. Its output never copies the private model candidate. The narrow fictional-ticket check additionally rejects a known excluded reference if it appears inside an approved field (including punctuation/case changes). **That check is not general-purpose confidential-data detection**: any other sensitive data accidentally approved by a reviewer can still appear.

No publish, mail, share, tool, connector, or external delivery endpoint exists. A `decisions` table stores metadata-only allowed/denied operation records. The browser-facing service is bound to **`127.0.0.1`** and is not intended to be internet accessible. All tests create a private temporary SQLite database and shut down their servers.

## Run and independently verify

From the repository root, with Python 3.12+ installed (the committed run used Python 3.13.5):

```bash
cd projects/P-006/6.1.1/req07-http-integration
python3 -m venv /tmp/p006-req07-check
PYTHONWARNINGS=error::ResourceWarning /tmp/p006-req07-check/bin/python -B -m unittest discover -s tests -v
/tmp/p006-req07-check/bin/python -B demo_receipts.py
sha256sum -c evidence/SHA256SUMS
```

For an isolated rerun, use a fresh `/tmp` environment name. The app and tests use **only Python's standard library**. No `pip install`, model server, Docker, external account, or internet connection is required. `demo_receipts.py` prints JSON with the result of six real HTTP and database cases. It generates a new run ID and timestamp, so compare the **decisions** with the archived receipts rather than expecting byte-for-byte identical JSON.

### Acceptance checks

| Test design | Expected HTTP/backend behavior |
| --- | --- |
| T03-A: bad private draft | Correct audience and reviewer approval give `READY`; the returned and SQLite-stored preview match the three approved facts, with no wrong `15:00` or ticket |
| T03-B: clean private draft | Same `READY` preview as A, demonstrating that preview content does not depend on candidate prose |
| T03-C: audience unconfirmed | `HELD`; separate SQLite read confirms no ready preview |
| T03-D: stale approval | Old revision receives HTTP `409`; preview stays `HELD` |
| T03-E: incomplete approved facts | Reviewer payload is rejected and preview stays `HELD` |
| T03-F: different confirmed audience | `HELD`; confirmation for service desk cannot authorize an employee-ready preview |
| Role and resource controls | Invalid token HTTP `401`; reviewer forbidden to create or preview; analyst forbidden to self-approve; another analyst cannot view/modify a different owner's notice |
| Invalidation and side effects | A new facts revision clears approval and ready state; publishing paths are nonexistent and respond `404`; authorized operations create metadata-only decision records |

**Independent observations:** The tests compare HTTP replies with records read through **a separate SQLite connection**. An API success message is not used as sole evidence that a state transition happened. The decision record contains actor alias, operation, action outcome and policy version, but not draft text or bearer tokens.

**Evidence interpretation:** The saved unittest transcript reports 20 test methods passed, not “20 vulnerabilities prevented” or proof of integrated Open WebUI security. The six demo variants are separately recorded in JSON. Both commands ran locally in this assistant's test container; the results are not claims about a running Open WebUI instance.

## Security boundaries, limits and follow-up

- This is a **teaching/reference service**, not a hardened authentication provider: tokens are generated/issued by the local test harness and not integrated with Open WebUI login or IAM. It uses unencrypted loopback HTTP and temporary local SQLite rather than production storage, session rotation, or audited durable identities.
- Caller authorization, approval and ready-state persistence are enforced in this standalone backend. The tests do **not** exercise actual Open WebUI chat, model routing, real model responses in this service, outbound network observation, or persistence beyond temporary local tests.
- `REQ-08` real event consumers, body logging, backups, access retention and expiry are **not** implemented or assessed here. The `decisions` table is a bounded demonstration receipt, not complete production telemetry.
- Before embedding the design into Open WebUI, verify the actual deployed version, authorization, proposed integration hook, owner/reviewer authority source, safe rendering, protected storage, logging, side effects, and all other gates in the original assessment plan. Do not merge arbitrary upstream changes or expose this demo externally.
- Preserve `B-04` and `B-05` **standalone-model FAIL** outcomes for the pinned earlier run; mark **Open WebUI integration and integrated REQ-07/REQ-08 as `NOT_TESTED`**. This HTTP-demo-only REQ-07 control passes its bounded, reproducible test suite.

**Review requirements:** Independently reproduce the suite and check that the saved HTTP/backend state supports its results; inspect authorization branches and excluded-marker limitations. Merge only after reviewer approval.

See [REQ-07 acceptance criteria](../security-requirements.md#p006-611-req-07--check-the-employee-ready-preview-outside-the-model), [T03 planned variants](../case-b-test-design.md#p006-611-t03--proposed-req-07-employee-ready-preview), and [previous source-only trust-boundary mapping](../trust-boundaries.md).
