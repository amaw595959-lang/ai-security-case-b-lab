# P-006 Phase B — Open WebUI preview integration design

**Lab** · P006-CASEB-LAB-01-B
**Canonical scope** · 6.1.2 architecture, 6.1.3 model route, 6.1.4 identity and authorization, and 6.1.5 deployment evidence
**Control** · Proposed P006-611-REQ-07 and INV-05. Reuse T03 A–F as written.

The program authorizes an isolated synthetic deployment in the task workspace. Use only the pinned Open WebUI source and image, the already verified local SmolLM2 artifact, and newly created fictional accounts and chats. The serving environment is temporary. The workspace owner and repository reviewers may see sanitized synthetic evidence. Customer systems, production data, external delivery, remote inference, and real accounts are outside scope. [6.1.1 closure](../../6.1.1/closure-report.md) · [Phase A report](https://github.com/amaw595959-lang/ai-security-case-b-lab/blob/1ddce3b233f7a4fd0f6edf2d0da4d246a3867c52/projects/P-006/6.1.3/phase-a-multi-model/report.md)

## Target and integration point

Pin upstream Open WebUI v0.13.4 at 0666e59d26a4d056e0bacee41742486badd71cf8 and the release's Linux amd64 manifest sha256:aa90751262a383d1279d76542fadab3a80c28b527f5415e9ed774182062525c1. Verify the running version, build hash, and installed module digest. Record the observed values separately from these source pins. [Upstream tree](https://github.com/open-webui/open-webui/tree/0666e59d26a4d056e0bacee41742486badd71cf8) · [Version endpoint](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/main.py#L2740-L2746)

Load an additive FastAPI router into the actual app process before the website fallback. Use native get_verified_user for every operation and its loaded user account and role. Open WebUI's administrator provisions the synthetic standard accounts. The router restricts analyst and reviewer privileges by lane and binds each notice to its owner and one assigned reviewer. Use native chat reads to verify the exact owner and private saved candidate. A caller-supplied identity, approval, source text, model response or readiness field grants no authority. The new tables belong to the extension. The upstream repository and installed upstream files stay unchanged. [Native role dependency](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/utils/auth.py#L570-L579) · [Administrator provisioning](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/routers/auths.py#L1056-L1094) · [Native chat lookup](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/models/chats.py#L1974-L1992)

~~~mermaid
flowchart LR
  A["Synthetic analyst"] -->|"session + ordinary private chat"| W["Pinned Open WebUI process"]
  R["Assigned synthetic reviewer"] -->|"session + reviewed facts"| W
  W -->|"loopback OpenAI-compatible completion"| M["Pinned SmolLM2"]
  W <-->|"private chat and account state"| C["Open WebUI SQLite"]
  W --> G["In-process REQ-07 router"]
  G <-->|"notice revision and scoped approvals"| D["Independent preview SQLite"]
  G -->|"ready or held + approved template"| A
~~~

The containers share a loopback-only network namespace. Open WebUI listens on 127.0.0.1:3000 and the sole configured provider is the local llama.cpp route at 127.0.0.1:8080/v1. The tester uses Docker exec inside that namespace. Create a fresh temporary application store and a separate SQLite notice store. No public port, production credential, sharing fixture or outbound tool is configured. Record exact effective settings and sanitized application/database evidence before claiming a result. [Native provider dispatch](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/main.py#L1690-L1709) · [Provider request](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/backend/open_webui/routers/openai.py#L1563-L1650)

## Decision rules

1. Let the native chat path save a private assistant candidate. Register a notice against the exact owner, chat and completed assistant message. Store its digest for the revision. The notice store needs no raw candidate copy.
2. Require the owner to confirm the intended audience with the current revision, then require the assigned reviewer to approve the three notice facts under REQ-07 for that revision and audience. Reject unknown fields, missing values and the known fictional ticket in approved text. A general confidential-data classifier is outside this exercise.
3. Re-check the owner and current private source reference on preview. Match confirmation, approval, audience, reviewer and revision. Generate the ready text from fixed formatting and the approved facts, with a transaction protecting the notice state. Keep all other outcomes held. Advancing the revision clears confirmation, approval and ready state.
4. Expose create, confirm, approve, revise and preview operations only. Record denial, handling of stale facts and output state. Compare native share, tool and automation tables before and after the test. Network isolation supplies separate evidence of the local route. Those observations cover this lab workflow and its enabled paths.

## Planned acceptance evidence

| Case | Expected result | Independent observation |
| --- | --- | --- |
| T03-A incorrect fixed candidate | READY only after both approvals, with the fixed approved notice | Content digest matches the private chat. Preview columns contain the approved facts and omit the fictional ticket and wrong time. |
| T03-B clean fixed candidate | Same READY text as A | Compare returned text and stored preview byte-for-byte. |
| T03-C, D, E and F | No ready preview for no confirmation, stale approval, incomplete facts or another audience | Check held state, revision and approval columns with a separate read-only SQLite connection. |
| Actual model route | Native Open WebUI returns and saves a real candidate from the intended model. Apply the same gate. | Correlate model alias and fingerprint, private chat owner and stored candidate digest, and returned/stored ready text. |
| Other identity, stale revision and unsupported action | No authority to view another analyst's preview or to impersonate the assigned reviewer. No publish route in the extension. | Inspect native user roles and the before-and-after notice, share, tool and automation state alongside the HTTP denials. |

Scope and planned assertions are preregistered here. Measured results and any unavailable evidence belong in the Phase B report.
